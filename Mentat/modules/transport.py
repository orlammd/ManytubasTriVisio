from mentat import Module

class Transport(Module):
    """
    Transport manager (tempo, time signature, klick pattern, playback)
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    def set_tempo(self, bpm):
        """
        Set tempo.
        Set sooperlooper's tempo and let jack transport do the rest (sl is transport master).
        Some delays are synced to the tempo as well.

        **Parameters**

        - `bpm`: beats per minute
        """

        self.engine.set_tempo(bpm)

        # self.engine.modules['Seq192'].set('tempo', bpm)
        # self.engine.modules['AudioLooper'].set('tempo', bpm)
        # self.engine.modules['Klick'].set('tempo', bpm)

        self.engine.modules['OpenStageControl'].set('tempo', bpm)

        # for mixer, strip in [
        #         ('BassFX', 'BassScape'),
        #         ('SynthsFX5Scape', 'SynthsFX5Scape')]:
        #     if strip in self.engine.modules[mixer].submodules:
        #         self.engine.modules[mixer].set(strip, 'Scape', 'bpm', bpm)
        #     else:
        #         # just in case non mixer infos are not loaded yet
        #         self.start_scene(strip + '_bpm', lambda: [
        #             self.wait(1, 's'), self.engine.modules[mixer].set(strip, 'Scape', 'bpm', bpm)
        #         ])

    def set_cycle(self, signature, pattern=None):
        """
        Set time signature (cycle length)

        **Parameters**

        - `signature`: musical time signature string ('4/4') or eigths per cycle number (legacy)
        - `pattern`:
            klick pattern (X = accented beat, x = normal beat, . = silence).
            If `None`, a default pattern is generated (straight quarter notes with an accent on beat 1)
        """

        if type(signature) in [float, int]:
            signature = '%s/8' % signature

        self.engine.set_time_signature(signature)

        eighths = int(self.engine.cycle_length * 2)

        if pattern is None:
            pattern = ''
            for i in range(eighths):
                if i == 0:
                    pattern += 'X'
                elif i % 2:
                    pattern += '.'
                else:
                    pattern += 'x'

        nom, denom = signature.split('/')
        # self.engine.modules['Klick'].set('cycle', int(nom), int(denom))
        # self.engine.modules['Klick'].set('pattern', pattern)
        #
        # self.engine.modules['Loop192'].set('cycle', eighths)
        # self.engine.modules['AudioLooper'].set('cycle', eighths)

        self.engine.modules['OpenStageControl'].set('signature', signature)

    def start(self):
        """
        Start transport.
        Tell seq192 to start and let jack transport do the rest.
        Klick is started manually.
        """

        self.engine.start_cycle()

        # self.engine.modules['Seq192'].start()
        #
        # # sooperlooper needs a cycle start hack
        # self.engine.modules['AudioLooper'].start()
        #
        # self.engine.modules['Klick'].start()

        self.engine.modules['OpenStageControl'].set('rolling', 1)

    def stop(self):
        """
        Stop transport.
        Tell seq192 to stop and let jack transport do the rest.
        Klick is stopped manually.
        """

        # self.engine.modules['Seq192'].stop()
        #
        # self.engine.modules['Klick'].stop()
        #
        self.engine.modules['OpenStageControl'].set('rolling', 0)
