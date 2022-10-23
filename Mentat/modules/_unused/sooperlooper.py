from mentat import Module

class Loop(Module):
    """
    Loop submodule (unnused)
    """

    def __init__(self, *args, loop_n, **kwargs):

        super().__init__(*args, **kwargs)

        # self.add_parameter('wet', '/sl/%i/set' % loop_n, 'sf', static_args=['wet'], default=0)

class SooperLooper(Module):
    """
    Audio looper
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.add_parameter('cycle', '/set', 'sf', static_args=['eighth_per_cycle'], default=8)
        self.add_parameter('tempo', '/set', 'sf', static_args=['tempo'], default=120)

        for i in range(16):
            loop = Loop('loop_%i' % i, loop_n=i, parent=self)

            self.add_submodule(loop)

            loop.add_parameter('n', None, 'i', default=i)
            loop.add_parameter('length', None, 'f', default=1)
            loop.add_parameter('position', None, 'f', default=0)

            loop.add_parameter('waiting', None, 'f', default=0)
            loop.add_parameter('recording', None, 'f', default=0)
            loop.add_parameter('overdubbing', None, 'f', default=0)
            loop.add_parameter('paused', None, 'f', default=0)
            loop.add_parameter('playing', None, 'f', default=0)

        self.pending_record = None

        self.add_event_callback('client_started', self.client_started)

    def client_started(self, name):
        """
        Subscribe to sl feedback when
        """
        if name == self.name or name == 'OpenStageControl':
            url = 'osc.udp://127.0.0.1:%i' % self.engine.port
            for feed in ['state', 'loop_len', 'loop_pos']:
                if name == self.name:
                    self.send('/sl/[0-7]/unregister_auto_update',feed, url, '/sl_feedback')
                    self.send('/sl/[0-7]/register_auto_update',feed, 50, url, '/sl_feedback')
                self.send('/sl/[0-7]/get',feed, url, '/sl_feedback')

    sl_states = {
        1: ['waiting', 'paused'],
        2: ['recording'],
        3: ['waiting', 'recording'],
        4: ['playing'],
        5: ['overdubbing'],
        14: ['paused']
    }
    def route(self, address, args):
        """
        Route sl feedback to loop modules' parameters
        """
        if address == '/sl_feedback':

            n, param, value = args

            if param == 'state':
                state = self.sl_states[value] if value in self.sl_states else []
                for p in ['waiting', 'recording', 'overdubbing', 'paused', 'playing']:
                    self.set('loop_%i' % n, p, 1 if p in state else 0)
            elif param == 'loop_len':
                self.set('loop_%i' % n, 'length', value)
            elif param == 'loop_pos' and self.get('loop_%i' % n, 'recording') == 0:
                self.set('loop_%i' % n, 'position', value)


        return False





    def start(self):
        """
        Reset cycle start position
        """
        self.send('/set', 'sync_source', 0)
        if self.pending_record is not None:
            self.send('/sl/%s/set' % self.pending_record, 'sync', 0)
            self.send('/sl/%s/hit' % self.pending_record, 'record')
            self.send('/sl/%s/set' % self.pending_record, 'sync', 1)
            self.pending_record = None
        self.send('/set', 'sync_source', -3)

    def reset(self, i='-1'):
        """
        Reset loop(s) (remove audio content and duration)

        **Parameters**

        - `i`:
            - loop number or
            - osc pattern to affect multiple loops (examples: '[1,2,5]', '[2-5]'...)
            - `-1` to affect all loops
        """
        self.send('/sl/%s/hit' % i, 'undo_all')

    def trigger(self, i='-1'):
        """
        Trig loop(s) (reset playback head to the beginning)

        **Parameters**

        - `i`:
            - loop number or
            - osc pattern to affect multiple loops (examples: '[1,2,5]', '[2-5]'...)
            - `-1` to affect all loops
        """
        self.send('/sl/%s/set' % i, 'sync', 0)
        self.send('/sl/%s/hit' % i, 'pause_off')
        self.send('/sl/%s/hit' % i, 'trigger')
        self.send('/sl/%s/set' % i, 'sync', 1)

    def record(self, i):
        """
        Start recording at next cycle.
        WARNING: record will not start before the beginning of the 3rd cycle after transport.start() was called/

        **Parameters**

        - `i`:
            - loop number or
            - osc pattern to affect multiple loops (examples: '[1,2,5]', '[2-5]'...)
            - `-1` to affect all loops
        """
        self.send('/sl/%s/hit' % i, 'record')

    def record_on_start(self, i):
        """
        Start recording next time transport.start() is called

        **Parameters**

        - `i`:
            - loop number or
            - osc pattern to affect multiple loops (examples: '[1,2,5]', '[2-5]'...)
            - `-1` to affect all loops
        """
        self.pending_record = i

    def overdub(self, i):
        """
        Start overdubing now

        **Parameters**

        - `i`:
            - loop number or
            - osc pattern to affect multiple loops (examples: '[1,2,5]', '[2-5]'...)
            - `-1` to affect all loops
        """
        self.send('/sl/%s/hit' % i, 'overdub')

    def pause(self, i='-1'):
        """
        Pause playback

        **Parameters**

        - `i`:
            - loop number or
            - osc pattern to affect multiple loops (examples: '[1,2,5]', '[2-5]'...)
            - `-1` to affect all loops
        """
        # self.send('/sl/%s/hit' % i, 'pause_off')
        self.send('/sl/%s/hit' % i, 'pause_on')

    def unpause(self, i='-1'):
        """
        Unpause playback

        **Parameters**

        - `i`:
            - loop number or
            - osc pattern to affect multiple loops (examples: '[1,2,5]', '[2-5]'...)
            - `-1` to affect all loops
        """
        self.send('/sl/%s/hit' % i, 'trigger')
