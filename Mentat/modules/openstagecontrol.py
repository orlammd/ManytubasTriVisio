from mentat import Module
from .nonmixer import NonMixer

import json
import urllib.parse
from inspect import getmembers, getdoc

class OpenStageControl(Module):
    """
    Open Stage Control touch interface.
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.osc_state = {}

        self.non_gui = {}
        self.ray_gui = {}

        self.add_parameter('session_loaded', None, types='i', default=0)
        self.add_parameter('session_populated', None, types='i', default=0)

        self.add_parameter('signature', '/signature', types='s', default='4/4')
        self.add_parameter('tempo', '/tempo', types='f', default=120)
        self.add_parameter('cursor', '/cursor', types='f', default=0)
        self.add_parameter('routes', '/routes', types='s', default='Loading')
        self.add_parameter('active_route', '/active_route', types='s', default='')
        self.add_parameter('route_methods', '/route_methods', types='s', default='')
        self.add_parameter('rolling', '/rolling', types='i', default=0)

        for post_process in ['pitch', 'filter']:
            for strip_type in ['voices', 'bass', 'synths', 'samples']:
                self.add_parameter('%s_%s' % (post_process, strip_type), None, types='i', default=1)

        self.add_event_callback('parameter_changed', self.parameter_changed)
        self.add_event_callback('client_started', self.client_started)
        self.add_event_callback('engine_started', lambda:
            self.set('routes', ','.join(self.engine.routes.keys()))
        )
        self.add_event_callback('engine_route_changed', self.engine_route_changed)

        self.start_scene('cycle_watch', self.cycle_watch)

    def cycle_watch(self):
        """
        Watch time to display global metric / cycle position
        """
        self.wait(0.04)
        engine = self.engine
        transport = self.engine.modules['Transport']
        while True:

            cursor = 0
            if self.get('rolling'):
                cycle_duration = 1000000000 * engine.cycle_length * 60 / engine.tempo
                cursor = ((engine.current_time - engine.cycle_start_time) % cycle_duration) / cycle_duration

            self.set('cursor', cursor)

            self.wait(0.04)

    def parameter_changed(self, module, name, value):
        """
        Whenever a parameter changes, send it to the interface:
            /module_name/submodule_name parameter_name *value

        and store that state locally.
        """
        if module == self:
            if name == 'session_loaded':
                self.set('session_populated', 0)
                if value == 1:
                    self.start_scene('populate_gui', self.populate_gui)

        # send state changes to OSC
        # /module_name param_name value
        address = '/' + '/'.join(module.module_path)
        if type(value) is not list:
            value = [value]

        self.send(address, name, *value)

        # store custom state
        if address not in self.osc_state:
            self.osc_state[address] = {}
        self.osc_state[address][name] = value

    def engine_route_changed(self, name):

        self.set('active_route', name)
        route = self.engine.active_route
        methods = [x for n,x in getmembers(route) if callable(x) and (hasattr(x, 'mk2_buttons') or hasattr(x, 'pedalboard_buttons'))]
        methods = sorted(methods, key=lambda m: m.index)

        data = []
        for m in methods:
            if route.name in m.__qualname__:
                btns = ''
                # if hasattr(m, 'mk2_buttons'): #### ORL -> normalement inutile
                #     btns += ''.join(['<div class="mk2">%s</div>' % x for x in m.mk2_buttons])
                if hasattr(m, 'pedalboard_buttons'):
                    btns += ''.join(['<div class="pb">%s</div>' % x for x in m.pedalboard_buttons])

                data.append({
                    'method': m.__name__,
                    'label': getdoc(m).split('\n')[0] if getdoc(m) else m.__name__,
                    'html': '%s' % btns
                })

        self.set('route_methods', json.dumps(data))




    def client_started(self, name):

        if self.get('session_loaded'):
            if self.get('session_populated') == 0:
                self.start_scene('populate_gui', self.populate_gui)

        self.send_state()


    def send_state(self):
        """
        Send local state (because it's not part of this module's actual state)
        """

        super().send_state()

        # send custom state
        for address in self.osc_state:
            for name in self.osc_state[address]:
                self.send(address, name, *self.osc_state[address][name])

    def resolve_path(self, path):
        """
        Resolve module path (see route())
        """
        module_name = path[0]

        if module_name == 'Engine':
            return self.engine
        elif module_name in self.engine.modules:
            mod = self.engine.modules[module_name]
            for n in path[1:]:
                if n in mod.submodules:
                    mod = mod.submodules[n]
            return mod
        return None

    def route(self, address, args):
        """
        Allow controlling any module parameter from the interface using the same syntax:
            /module_name/submodule_name parameter_name *value
        or calling a module method:
            /module_name/submodule_name/call method_name *args
        """

        if address == '/keyboard':
            self.engine.modules['OpenStageControlKeyboardOut'].send(*args)
            return False

        # send OSC controls to modules
        # /module_name param_name value
        module_path = address.split('/')[1:]
        module_name = module_path[0]

        call = False
        if module_path[-1] == 'call':
            module_path = module_path[:-1]
            call = True

        mod = self.resolve_path(module_path)

        if mod is not None:

            if call:
                if len(args) > 0 and type(args[0] == str) and hasattr(mod, args[0]):
                    method = getattr(mod, args[0])
                    if callable(method):
                        method(*args[1:])
            else:

                if type(args[0]) == str:
                    mod.set(*args)

            return False


    def populate_gui(self):
        """
        Here be dragons.

        Generates a gui for all non mixers instance.

        Maybe this could be extended to all modules.
        Maybe this is overkill.
        """

        while self.get('session_loaded') == 0:
            self.wait(2, 's')

        panel = {'tabs': [], 'verticalTabs': True, 'bypass': True}

        for name, mod in self.engine.modules.items():
            if isinstance(mod, NonMixer):
                tab = {
                    'type': 'tab',
                    'id': 'non-mixer.%s' % name,
                    'label': name,
                    'layout': 'horizontal',
                    'innerPadding': False,
                    'widgets': [],
                    'padding': 1,
                    'contain': False
                }
                panel['tabs'].append(tab)
                for sname, smod in mod.submodules.items():
                    strip = {
                        'type': 'panel',
                        'layout': 'vertical',
                        'width': 120,
                        'widgets': [],
                        'innerPadding': True,
                        'lineWidth': 0,
                        'css': 'class: strip;',
                        'html': '<div class="label center">%s</div>' % urllib.parse.unquote(sname),
                        'scroll': False
                    }
                    tab['widgets'].append(strip)
                    plugins = {
                        'type': 'panel',
                        'layout': 'vertical',
                        'height': 120,
                        'widgets': [],
                        'innerPadding': True,
                        'padding': 4,
                        'css': 'class: carved;',
                        'scroll': True,
                        'contain': False
                    }
                    strip['widgets'].append(plugins)
                    plugs = {}
                    for plugname, plugmod in smod.submodules.items():
                        if plugname != 'Gain':
                            if plugname not in plugs:
                                modal = {
                                    'type': 'modal',
                                    'label': urllib.parse.unquote(plugname),
                                    'popupLabel': '%s > %s' % (urllib.parse.unquote(sname), urllib.parse.unquote(plugname)),
                                    'layout': 'horizontal',
                                    'height': 30,
                                    'css': 'class: plugin-modal',
                                    'popupPadding': 1,
                                    'innerPadding': True,
                                    'popupHeight': 400,
                                    'popupWidth': 800,
                                    'widgets': []
                                }
                                plugs[plugname] = modal
                                plugins['widgets'].append(modal)

                            for pname in plugmod.parameters:

                                param = plugmod.parameters[pname]
                                modal['widgets'].append({
                                    'type': 'panel',
                                    'layout': 'vertical',
                                    'css': 'class: strip',
                                    'html': '<div class="label center">%s</div>' % urllib.parse.unquote(pname),
                                    'width': 120,
                                    'widgets': [
                                        {
                                            'type': 'knob',
                                            'horizontal': True,
                                            'pips': True,
                                            'range': {'min': {'%.1f' % param.range[0]: param.range[0]}, 'max': {'%.1f' % param.range[1]: param.range[1]}},
                                            'value': param.args[0],
                                            'default': param.args[0],
                                            'doubleTap': True,
                                            'linkId': param.address,
                                            'address': '/%s/%s/%s' % (name, sname, plugname),
                                            'preArgs': pname,
                                            'decimals': 5,
                                            'pips': True,
                                            'expand': True,
                                            'design': 'solid'
                                        },
                                        {
                                            'type': 'input',
                                            'width': 120,
                                            'decimals': 5,
                                            'linkId': param.address,
                                            'bypass': True
                                        }
                                    ]
                                })

                    strip['widgets'].append({
                    'type': 'button',
                    'label': 'Mute',
                    'colorWidget': 'var(--yellow)',
                    'css': 'class: discrete;',
                    'value': smod.get('Gain', 'Mute'),
                    'address': '/%s/%s/Gain/Mute' % (name, sname)
                    })
                    strip['widgets'].append({
                        'type': 'fader',
                        'range': {'min': -70, '6%': -60, '12%': -50, '20%': -40, '30%': -30, '42%': -20, '60%': -10, '80%': 0, 'max': 6 },
                        'expand': True,
                        'doubleTap': True,
                        'pips': True,
                        'design': 'round',
                        'value': smod.get('Gain', 'Gain'),
                        'default': smod.get('Gain', 'Gain'),
                        'address': '/%s/%s/Gain/Gain' % (name, sname),
                        'linkId': '/%s/%s/Gain/Gain' % (name, sname)
                    })
                    strip['widgets'].append({
                        'type': 'input',
                        'width': 120,
                        'decimals': 5,
                        'linkId': '/%s/%s/Gain/Gain' % (name, sname),
                        'bypass': True
                    })

        self.edit_gui('non-mixers', panel)



        ray = self.engine.modules['RaySession']
        panel = {'widgets': [], 'layout': 'vertical', 'padding': 1, 'innerPadding': False, 'contain': False}
        for p in ray.parameters:
            if 'status_' in p:
                name = p[7:]
                strip = {'type': 'panel', 'layout': 'horizontal', 'css': 'class: strip;', 'height': 40, 'padding': 4,'widgets' : [
                    {
                        'type': 'text',
                        'align': 'left',
                        'address': '/RaySession',
                        'preArgs': 'label_%s' % name,
                        'expand': True
                    },
                    {
                        'type': 'button',
                        'label': '^play',
                        'mode': 'momentary',
                        'colorWidget': 'var(--green)',
                        'css': '#{@{status_%s} ? \'class: on;\': \'\'}' % name,
                        'address': '/RaySession/call',
                        'preArgs': ['send', '/ray/client/start', name]
                    },
                    {
                        'type': 'variable',
                        'id': 'status_%s' % name,
                        'address': '/RaySession',
                        'preArgs': ['status_%s' % name]
                    },
                    {
                        'type': 'button',
                        'label': '^stop',
                        'mode': 'momentary',
                        'colorWidget': 'var(--red)',
                        'address': '/RaySession/call',
                        'preArgs': ['send', '/ray/client/stop', name]
                    }

                ]}
                panel['widgets'].append(strip)



        self.edit_gui('ray-session', panel)

        self.set('session_populated', 1)
        self.send_state()

    def edit_gui(self, widget, data):
        """
        Send data to interface, split it into small chunks that udp can handle.
        """
        blob = json.dumps(data)

        self.send('/EDIT_QUEUE/START', widget)
        size = 1024 * 16
        i = 0

        while True:
            bits = blob[i:i+size]
            self.send('/EDIT_QUEUE/APPEND', widget, bits)
            if i >= len(blob):
                break
            i += size

        self.send('/EDIT_QUEUE/END', widget)


    def transport_start(self):
        """
        Start transport and trigger rolling loops
        """
        if self.get('rolling'):
            for loop in self.engine.modules['AudioLooper'].submodules.values():
                if loop.get('playing'):
                    self.engine.modules['AudioLooper'].trigger(loop.get('n'))


        self.engine.modules['Transport'].start()

    def transport_stop(self):
        """
        Stop transport and loops
        """
        self.engine.modules['Transport'].stop()
        self.engine.active_route.pause_loopers()

    def panic(self):
        self.engine.modules['ZHiSynths'].send('/Panic')
        self.engine.modules['ZLowSynths'].send('/Panic')
        self.engine.modules['HiCSynths'].send('/panic')
        self.engine.modules['LowCSynths'].send('/panic')

    def route_method(self, name):

        if hasattr(self.engine.active_route, name):
            m = getattr(self.engine.active_route, name)
            if callable(m):
                if hasattr(m, 'mk2_buttons'):
                    self.engine.active_route.route('osc', None, '/mk2/button', list(m.mk2_buttons.keys())[:1])
                elif hasattr(m, 'pedalboard_buttons'):
                    self.engine.active_route.route('osc', None, '/pedalboard/button', list(m.pedalboard_buttons.keys())[:1])

    def set_pitch(self, value):

        strips = []
        if self.get('pitch_voices') == 1:
            strips.append('Vocals*')
        if self.get('pitch_bass') == 1:
            strips.append('Bass*')
        if self.get('pitch_synths') == 1:
            strips.append('Synths')
        if self.get('pitch_samples') == 1:
            strips.append('Samples*')

        if strips:
            self.engine.modules['PostProcess'].set_pitch(strips, value)


    def set_filter(self, value):

        strips = []
        if self.get('filter_voices') == 1:
            strips.append('Vocals*')
        if self.get('filter_bass') == 1:
            strips.append('Bass*')
        if self.get('filter_synths') == 1:
            strips.append('Synths')
        if self.get('filter_samples') == 1:
            strips.append('Samples*')

        if strips:
            self.engine.modules['PostProcess'].set_filter(strips, value)
