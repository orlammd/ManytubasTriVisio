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

    @pedalboard_button(2)
    def intro(self):
        """
        INTRO
        """
        pytaVSL.trijc_io()
        # self.start_sequence('aight', [{
        #     1: lambda: [pytaVSL.animate('Back', 'scale', [0.5, 0.5], [0.7, 0.7], 4, 's', 'linear')],
        #     2: lambda: [pytaVSL.animate('TriJC_*', 'position', None, [0.7, 0.7, 0.7],5, 's', 'linear')],
        #     3: lambda: [pytaVSL.animate('t_TriJC_*', 'rotate', [10, -40, 0], [30, 30, 30], 8, 's', 'linear')],
        #     4: lambda: [pytaVSL.animate('ot_TriJC_*', 'rgbwave', None, 0.5, 3, 's', 'linear')],
        # },
        # {1: lambda: pytaVSL.animate('*', 'rotate_z', 30, -880, 3)}], loop=True)

    @pedalboard_button(3)
    def intro2(self):
        """
        INTRO
        """
        pytaVSL.trijc_io('out')
        # self.start_sequence('aight', [{
        #     1: lambda: [pytaVSL.animate('Back', 'scale', [0.5, 0.5], [0.7, 0.7], 4, 's', 'linear')],
        #     2: lambda: [pytaVSL.animate('TriJC_*', 'position', None, [0.7, 0.7, 0.7],5, 's', 'linear')],
        #     3: lambda: [pytaVSL.animate('t_TriJC_*', 'rotate', [10, -40, 0], [30, 30, 30], 8, 's', 'linear')],
        #     4: lambda: [pytaVSL.animate('ot_TriJC_*', 'rgbwave', None, 0.5, 3, 's', 'linear')],
        # },
        # {1: lambda: pytaVSL.animate('*', 'rotate_z', 30, -880, 3)}], loop=True)
