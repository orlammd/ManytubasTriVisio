from ..base import RouteBase, pedalboard_button
from .video import Video
from .light import Light

from modules import *

class Chapitre1(Video, Light, RouteBase):

    def activate(self):
        """
        Called when the engine switches to this route.
        """

        super().activate()

        transport.set_tempo(150)
        transport.set_cycle('4/4', pattern="Xxxx")

        # Setups, banks...
        prodSampler.set_kit(self.name)


    @pedalboard_button(1)
    def stop(self):
        """
        STOP
        """
        transport.stop()
        self.pause_loops()

    @pedalboard_button(2)
    def intro(self):
        """
        INTRO
        """
        pass
