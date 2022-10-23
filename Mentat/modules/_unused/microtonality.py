from mentat import Module

class MicroTonality(Module):
    """
    Microtonality manager for autotunes, zyn synths and calf synths.
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.autotunes = ['NanoMeuf', 'NanoNormo', 'NanoGars', 'KeschMeuf', 'KeschNormo', 'KeschGars']
        self.zynsynth = 'ZHiSynths'
        self.calfpitcher = 'CalfPitcher'

    def enable(self):
        """
        Enable microtonality
        """
        modules = self.engine.modules

        modules[self.zynsynth].set('microtonality', True)


    def disable(self):
        """
        Disable microtonality
        """
        modules = self.engine.modules

        self.set_tuning(*[0.0 for i in range(12)])

        modules[self.zynsynth].set('microtonality', False)


    def set_tuning(self, *tuning):
        """
        Set per-note tuning for autotunes, zyn synths and calf synths.

        **Parameters**

        - `*tunings`: 12 float arguments between -1 (-1 semi-tone) and 1 (+1 semi-tone)
        """

        modules = self.engine.modules

        # zyn
        zyntuning = tuning[10:] + tuning[:10] # zyn commence au Si bémol
        modules[self.zynsynth].set('tuning', "\n".join([str(100.0 + i * 100 + zyntuning[i] * 100) for i in range(12)]).replace('1200.0', '2/1'))

        # calf
        modules[self.calfpitcher].set('tuning', *tuning)

        # autotuner
        for at in self.autotunes:
            modules[at].set_tuning(*tuning)
