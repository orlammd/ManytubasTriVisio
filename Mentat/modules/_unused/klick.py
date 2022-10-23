from mentat import Module

class Klick(Module):
    """
    Metronom, your only true friend.
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.add_parameter('pattern', '/klick/simple/set_pattern', 's', default='X.x.x.x.')
        self.add_parameter('tempo', '/klick/simple/set_tempo', 'f', default=120)
        self.add_parameter('cycle', '/klick/simple/set_meter', 'ii', default=[8,8])


    def start(self):
        """
        Start metronom
        """
        self.send('/klick/metro/start')

    def stop(self):
        """
        Stop metronom
        """
        self.send('/klick/metro/stop')
