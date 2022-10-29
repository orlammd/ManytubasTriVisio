# import Route base class
from mentat import Route

# import engine & modules objects
# so that they can be used in the routing
from modules import *

from inspect import getmembers

method_index = 0
class pedalboard_button():
    """
    Decorator for route methods that can be called directly
    from pedalboard button messages
    """
    def __init__(self, button):
        self.button = button
    def __call__(self, method):
        if not hasattr(method, 'index'):
            global method_index
            method.index = method_index
            method_index += 1
        if not hasattr(method, 'pedalboard_buttons'):
            method.pedalboard_buttons = {}
        method.pedalboard_buttons[self.button] = True
        return method

class RouteBase(Route):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.direct_routing = {
            '/pedalboard/button': {},
        }

        for name, method in getmembers(self):
            if hasattr(method, 'pedalboard_buttons'):
                for button in method.pedalboard_buttons:
                    if button not in self.direct_routing['/pedalboard/button']:
                        self.direct_routing['/pedalboard/button'][button] = []
                    self.direct_routing['/pedalboard/button'][button].insert(0, method)

            # if hasattr(method, 'mk2_buttons'):
            #     for button in method.mk2_buttons:
            #         if button not in self.direct_routing['/mk2/button']:
            #             self.direct_routing['/mk2/button'][button] = []
            #         self.direct_routing['/mk2/button'][button].insert(0, method)
            #         self.mk2_lights[button] = method.mk2_buttons[button]

    def activate(self):
        # mk2Control.set_lights(self.mk2_lights)
        super().activate()


    def route(self, protocol, port, address, args):
        """
        Base routing for all routes
        """
        if address in self.direct_routing:
            if len(args) > 0 and args[0] in self.direct_routing[address]:
                for method in self.direct_routing[address][args[0]]:
                    method()

        if address == '/set_route':
            engine.set_route(args[0])

        if address == '/load_slides_from_dir':
            if len(args) > 0:
                pytaVSL.load_slides_from_dir(args[0])
            else:
                pytaVSL.load_slides_from_dir()

        if address == '/save_state':
            """
            Save state omitting default values
            args: chapter
            """
            pytaVSL.save_state(args[0])

        if address == '/position_overlay':
            overlay = 'Common'
            if len(args) > 0:
                overlay = args[0]
            pytaVSL.position_overlay(overlay)

        if address == '/trijc_io':
            self.logger.info('trijc_io osc trigged')
            pytaVSL.trijc_io(*args)

        if '/pyta' in address:
            pytaVSL.send(address, *args)



    def start_sequence(self, name, sequence, loop=True):
        """
        Start scene with sequence prefix and self.play_sequence() as method

        **Parameters**

        - `name`: name of sequence
        - `sequence`: see Route.play_sequences()
        - `loop`: see Route.play_sequences()
        """
        self.start_scene('sequences/%s' % name, self.play_sequence, sequence, loop)

    def stop_sequence(self, name):
        """
        Stop scene with sequence prefix

        **Parameters**

        - `name`: name of sequence
        """
        self.stop_scene('sequences/%s' % name)

    def resetFX(self):
        """
        Reset effects
        """
        # # BassFX
        # for name in bassFX.meta_parameters:
        #     bassFX.set(name, 'off')
        #
        #
        # for name, mod in engine.modules.items():
        #
        #     # SynthsFX
        #     if 'SynthsFX' in name:
        #
        #         for name in mod.submodules:
        #             # Ins
        #             if name not in mod.name:
        #                 mod.set(name, 'Gain', 'Gain', -70.0)
        #
        #         # Outs
        #         mod.set(mod.name, 'Gain', 'Mute', 1.0)
        #
        #
        #     # SamplesFX
        #     elif 'SamplesFX' in name:
        #         for i in range(1,6):
        #             # Ins
        #             mod.set('Samples' + str(i), 'Gain', 'Gain', -70.0)
        #
        #         # Outs
        #         mod.set(name, 'Gain', 'Mute', 1.0)
        #
        #     # VocalsFX
        #     elif 'VocalsNanoFX' in name or 'VocalsKeschFX' in name:
        #         for name in mod.submodules:
        #             # Ins
        #             if name not in mod.name:
        #                 mod.set(name, 'Gain', 'Gain', -70.0)
        #         # Outs
        #         mod.set(name, 'Gain', 'Mute', 1.0)


        postprocess.set_filter('*', 24000)
        postprocess.set_pitch('*', 1)

    # def resetSamples(self):
    #     """
    #     Reset (mute) all samples
    #     """
    #     for i in range (1,6):
    #         samples.set('Samples' + str(i), 'Gain', 'Mute', 1.0)

    def pause_loops(self):
        """
        Pause loopers and looped scenes (sequences)
        """
        # stop all mentat sequences
        self.stop_sequence('*')

    # def reset(self):
    #     """
    #     Reset samples and effects
    #     """
    #     self.resetFX()
    #     self.resetSamples()
    #
    #     for name in outputs.submodules:
    #         outputs.submodules[name].set('Gain', 'Mute', 0)
