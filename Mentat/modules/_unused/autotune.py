from mentat import Module

class Autotune(Module):
    """
    Autotuner (x42-fat1)
    """

    def __init__(self, *args, offset=0.0, **kwargs):

        super().__init__(*args, **kwargs)

        for i in range(12):
            self.add_parameter('note_%i' % i, '/x42/parameter', 'if', static_args=[i + 9], default=1.0)
            self.add_parameter('tuning_%i' % i, '/x42/parameter', 'if', static_args=[i + 26], default=0.0)

        self.add_parameter('mode',      '/x42/parameter', 'if', static_args=[0], default=2.0) # manual
        self.add_parameter('tuning',    '/x42/parameter', 'if', static_args=[2], default=440.0)
        self.add_parameter('bias',      '/x42/parameter', 'if', static_args=[3], default=0.0)
        self.add_parameter('filter',    '/x42/parameter', 'if', static_args=[4], default=0.02)
        self.add_parameter('correction','/x42/parameter', 'if', static_args=[5], default=1.0)
        self.add_parameter('offset',    '/x42/parameter', 'if', static_args=[6], default=offset)
        self.add_parameter('fastmode',  '/x42/parameter', 'if', static_args=[8], default=1.0)

        self.base_offset = offset
        self.pitch_value = 1.0

        def pitch_getter(offset):
            return self.pitch_value

        def pitch_setter(pitch):

            if pitch < 1:
                val = pitch * 24 / 0.75 + (-24 / 0.75)
            elif pitch >= 1:
                val = pitch * 12 - 12

            self.pitch_value = pitch
            self.set('offset', val + self.base_offset)

        self.add_meta_parameter('pitch',  ['offset'], pitch_getter, pitch_setter)


    def set_notes(self, *notes):
        """
        Set allowed notes for the autotuner.

        **Parameters**

        - `*notes`: 12 int arguments that can be either 1 (allowed) or 0 (disallowed)
        """
        i = 0
        for note in notes:
            self.set('note_%i' % i, note)
            i += 1

    def set_tuning(self, *tunings):
        """
        Set per-note tuning.

        **Parameters**

        - `*tunings`: 12 float arguments between -1 (-1 semi-tone) and 1 (+1 semi-tone)
        """
        i = 0
        for tuning in tunings:
            self.set('tuning_%i' % i, tuning)
            i += 1
