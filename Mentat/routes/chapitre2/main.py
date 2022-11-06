from ..base import RouteBase, pedalboard_button
from .video import Video
from .light import Light

from modules import *

class Chapitre2(Video, Light, RouteBase):

    def activate(self):
        """
        Called when the engine switches to this route.
        """

        super().activate()

        transport.set_tempo(150)
        transport.set_cycle('4/4', pattern="Xxxx")

        # Setups, banks...
        prodSampler.set_kit(self.name)

        self.start_scene('init_chapitre2', lambda: [
            # Overlay
            self.init_pyta(),
            self.wait(0.2, 's'),

            # Chapitre 2
            self.m_ch2_1()
        ])

    def init_pyta(self):
        # Degroupage des TV
        #### A priori inutile ?

        # Reset des slides
        pytaVSL.reset()

        # def create_tv_groups():
        pytaVSL.create_group('tv_jc', ['plane_horn_jc', 'p_jc'])
        #     for index in range(1,5):
        #         pytaVSL.create_group('tv' + str(index), ['plane_horn_' + str(index), ',p_ch1-' + str(index+2)])

        chapter = 'ch2'
        self.start_scene('groups_and_overlay', lambda: [
            # Chargement de l'overlay commun
            pytaVSL.position_overlay('Common'),

            ### Création des groupes du chapitre
            pytaVSL.create_group('m_iraye', ['m_layout', 'm_' + chapter + '*']),
            pytaVSL.create_group('f_arabesques', ['f_arabesque*']),
            self.wait(0.1, 's'),
            pytaVSL.create_group('f_ilm', ['f_arabesques', 'f_' + chapter + '*']),
            # create_tv_groups(),
            pytaVSL.check_new_slides(once=True),
            self.wait(0.1, 's'),
            pytaVSL.position_overlay('Chapitre2'),

        ])

    @pedalboard_button(100)
    def m_ch2_1(self):
        """
        Miraye Intro Chapitre 2
        """
        self.start_scene('sequence/lancement_miraye_1', lambda: [
            ### Lancement du Film
            pytaVSL.trijc_io('in', 'lustre', 1, 'elastic'),
            self.wait(2, 's'),
            pytaVSL.trijc_change_tool('tuba'),
            self.wait(0.3, 's'),
            pytaVSL.miraye_in('m_ch2-1', 1)
            ]
        )

    @pedalboard_button(1)
    def jingle_jc_1(self):
        """
        Jingle intempestif #1
        """
        pytaVSL.jc_jingle_io('bottom', 0.3, 'elastic-inout')
