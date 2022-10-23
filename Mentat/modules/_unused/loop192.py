from mentat import Module

class Loop192(Module):
    """
    Midilooper
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.add_parameter('cycle', '/set', 'sf', static_args=['eighth_per_cycle'], default=8)
        self.add_parameter('tempo', '/set', 'sf', static_args=['tempo'], default=120)

    def start(self):
        """
        Start playback
        """
        self.send('/play')

    def stop(self):
        """
        Stop playback
        """
        self.send('/stop')
