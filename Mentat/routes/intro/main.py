from ..base import RouteBase, pedalboard_button
from .video import Video
from .light import Light

from modules import *

class Intro(Video, Light, RouteBase):

    def activate(self):
        """
        Called when the engine switches to this route.
        """

        super().activate()

        transport.set_tempo(60)
        transport.set_cycle('4/4', pattern="Xxxx")

        # Setups, banks...
        prodSampler.set_kit(self.name)

        self.start_scene('load_and_overlay', lambda: [
            pytaVSL.load_slides_from_dir('Common'),
            self.wait(0.5, 's'),
            pytaVSL.position_overlay('Common')
        ])

    def intro(self):
        """
        INTRO
        """
        pass
