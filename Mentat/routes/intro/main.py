from ..base import RouteBase, mk2_button, pedalboard_button
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

        pytaVSL.load_slides_from_dir('Common')

    def overlay(self):
        """
        Positionning slides in overlay
        """
        pytaVSL.set('back', 'position', [])

    def intro(self):
        """
        INTRO
        """
        pass
