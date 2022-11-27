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

        transport.set_tempo(60)
        transport.set_cycle('4/4', pattern="Xxxx")

        # Setups, banks...
        prodSampler.set_kit(self.name)

        self.start_scene('init_chapitre4', lambda: [
            # Overlay
            self.init_chapitre4(),

            # Chapitre 3
            self.m_ch4_1()
        ])

    def init_chapitre4(self):



        chapter = 'ch4'

        ### Création des groupes du chapitre
        # pytaVSL.create_group('tv1', ['plane_horn_1','p_' + chapter + '-3']) # Soft & Rains dans le journal

        pytaVSL.create_group('m_iraye', ['m_layout', 'm_' + chapter + '*'])
        pytaVSL.create_group('f_arabesques', ['f_arabesque_1', 'f_arabesque_2'])
        pytaVSL.create_group('f_arabesques_2', ['f_arabesque_3', 'f_arabesque_4'])
        pytaVSL.create_group('f_arabesques_3', ['f_arabesque_5', 'f_arabesque_6'])
        pytaVSL.create_group('f_ilm', ['f_arabesques', 'f_' + chapter + '*'])

        pytaVSL.sync()

        pytaVSL.position_overlay('Chapitre4')

    @pedalboard_button(100)
    def m_ch4_1(self):
        """
        Intro Miraye
        """
        pass
