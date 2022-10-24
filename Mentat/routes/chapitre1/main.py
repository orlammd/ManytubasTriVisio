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

        # Chargement des vidéos
        pytaVSL.load_slides_from_dir('Chapitre1')

    @pedalboard_button(1)
    def aspipub(self):
        """
        Aspiration des pubs
        """

        self.start_scene('sequences/aspipub', lambda: [
            pytaVSL.trijc_io('in', 2, 'linear'),
            self.wait(4, 's'),
            ### ASPIRATION
            self.wait(1, 's'),
            pytaVSL.trijc_io('out', 1, 'elastic'),
            self.wait(1.2, 's'),
            pytaVSL.trijc_io('in', 1, 'elastic'),
            self.wait(1.2, 's'),
            pytaVSL.miraye_in('ch1-1', 1)
            ]
        )

    @pedalboard_button(2)
    def test(self):
        """
        INTRO
        """
        self.start_scene('sequences/aspipub', lambda: [
            [
                pytaVSL.sanimate_prop('ch1-1', 'warp_1', [0, 0, 0, -0.49, 1, 'elastic']), pytaVSL.sanimate_prop('ch1-1', 'warp_4', [0, 0, 0, 0.49, 1, 'elastic']),
                pytaVSL.sanimate_prop('MirayeLayout', 'warp_1', [0, 0, 0, -0.49, 1, 'elastic']), pytaVSL.sanimate_prop('MirayeLayout', 'warp_4', [0, 0, 0, 0.49, 1, 'elastic'])
                ],
            self.wait(0.8, 's'),
            pytaVSL.sanimate_prop('mirayelayout', 'zoom', [0.7, 0.035, 1, 'elastic' ]), pytaVSL.sanimate_prop('mirayelayout', 'position', [0, 0, 0, -0.3, -0.2, 0, 0.5, 'elastic']),
            pytaVSL.sanimate_prop('ch1-1', 'zoom', [0.7, 0.035, 1, 'elastic' ]), pytaVSL.sanimate_prop('ch1-1', 'position', [0, 0, 0, -0.3, -0.2, 0, 0.5, 'elastic']),
        ])

    @pedalboard_button(3)
    def outro(self):
        """
        OUTRO
        """
        pytaVSL.trijc_io('out')

    @pedalboard_button(4)
    def m_intro(self):
        """
        INTRO MIREILLE
        """
        pytaVSL.miraye_in()
