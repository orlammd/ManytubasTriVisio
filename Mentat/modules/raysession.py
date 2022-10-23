from mentat import Module

#from .alsapatch import AlsaPatcher #### ORL à enlever normalement

import os
import json

class RaySession(Module):
    """
    RaySession (Non Session Manager) monitor.
    Keeps track of clients states and keep mentat modules in sync with them.
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.client_init = []

        # self.alsa_patcher = AlsaPatcher('AlsaPatcher')
        # self.alsa_patcher.load('%s/RaySessions/PlagiatLive/PlagiatLive.alsapatch' % os.getenv('PLAGIAT_SETUP_DIR'))
        # self.alsa_patcher.connect()

        self.send('/ray/server/monitor_quit')
        self.send('/ray/server/monitor_announce')

    def route(self, address, args):

        if address == '/ray/monitor/client_state':
            name = args[0]
            status = args[1]

            self.register_client(name)

            if status:
                self.client_started(name)
            else:
                self.client_stopped(name)

        elif address == '/ray/monitor/client_event':
            name = args[0]
            event = args[1]

            self.register_client(name)

            if event == 'ready' or event == 'started':
                if self.get('status_%s' % name) == 0:
                    self.client_started(name)

            elif event == 'stopped_by_server' or event == 'client_stopped_by_server':
                self.client_stopped(name)
            elif event == 'stopped_by_itself' or event == 'client_stopped_by_itself':
                self.client_stopped(name)
                self.info('module %s crashed')
                os.popen('dunstify -u critical -a Mentat -t 0 "%s" "a crashé"' % name)

        elif address == '/reply':
            if len(args) > 1 and args[0] == '/ray/client/get_properties':
                props = {}
                for line in args[1].split('\n'):
                    key, _, val = line.partition(':')
                    props[key] = val
                if len(props['label']) == 0:
                    props['label'] = props['client_id']
                self.set('label_%s' % props['client_id'], props['label'])

        return False

    def register_client(self, name):
        if 'status_%s' % name not in self.parameters:
            self.add_parameter('status_%s' % name, None, types='i', default=0)
            self.add_parameter('label_%s' % name, None, types='s', default=name)
            self.send('/ray/client/get_properties', name)

    def client_started(self, name):

        self.set('status_%s' % name, 1)

        if name in self.engine.modules:
            module = self.engine.modules[name]
            if name not in self.client_init:
                # first start: load default state if any
                # module.load('default')
                self.client_init.append(name)
            else:
                # restart: send state
                self.logger.info('client %s restarted, sending state' % name)
                module.send_state()
            self.engine.dispatch_event('client_started', name)

        # self.alsa_patcher.connect()


    def client_stopped(self, name):

        self.set('status_%s' % name, 0)
