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

        transport.set_tempo(60)
        transport.set_cycle('4/4', pattern="Xxxx")

        # Setups, banks...
        prodSampler.set_kit(self.name)

        self.start_scene('init_chapitre2', lambda: [
            # Overlay
            self.init_chapitre2(),
            self.wait(0.2, 's'),

            # Chapitre 2
            self.m_ch2_1()
        ])

    def init_chapitre2(self):
        # Degroupage des TV
        #### A priori inutile ?

        # Reset des slides
        pytaVSL.reset()

        # def create_tv_groups():
        pytaVSL.create_group('tv_jc', ['plane_horn_jc', 'p_jc'])
        # for index in range(1,5):
        pytaVSL.create_group('tv1', ['plane_horn_1','p_ch2-5']) # Pub Paillassons

        chapter = 'ch2'
        self.start_scene('groups_and_overlay', lambda: [
            # Chargement de l'overlay commun
            pytaVSL.position_overlay('Common'),

            ### Création des groupes du chapitre
            pytaVSL.create_group('m_iraye', ['m_layout', 'm_' + chapter + '*']),
            pytaVSL.create_group('f_arabesques', ['f_arabesque_1', 'f_arabesque_2']),
            pytaVSL.create_group('f_arabesques_2', ['f_arabesque_3', 'f_arabesque_4']),
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
        self.start_scene('sequence/miraye_intro_chapitre_2', lambda: [
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
        self.start_scene('sequence/jingle_intempestif_1', lambda: [
            pytaVSL.jc_jingle_io('bottom', 0.3, 'elastic-inout'),
            self.wait(0.3, 's'),
            pytaVSL.set('m_ch2-1', 'video_speed', 0),
            self.wait(pytaVSL.get('p_jc', 'video_end') - 0.2, 's'),
            self.m_ch2_2()
        ])

    @pedalboard_button(101)
    def m_ch2_2(self):
        """
        Miraye Intro Chapitre 2 (2)
        """
        self.start_scene('sequence/miraye_intro_chapitre_2_2', lambda: [
            pytaVSL.m_switch_video('m_ch2-1', 'm_ch2-2')
        ])
        ###### TODO : m_ch2-2 à séparer en deux parties.

    @pedalboard_button(2)
    def jingle_jc_2(self):
        """
        Jingle intempestif #2
        """
        self.start_scene('sequence/jingle_intempestif_2', lambda: [
            pytaVSL.jc_jingle_io('top', 0.15, 'elastic-inout'),
            pytaVSL.set('m_ch2-2', 'video_speed', 0),
            self.wait(pytaVSL.get('p_jc', 'video_end'), 's'),
            self.m_ch2_3()
        ])

    @pedalboard_button(102)
    def m_ch2_3(self):
        """
        Miraye Intro Chapitre 2 (3)
        """
        self.start_scene('sequence/miraye_intro_chapitre_2_3', lambda: [
            pytaVSL.m_switch_video('m_ch2-2', 'm_ch2-3'),
            self.wait(4, 's'), # TODO affiner le timing
            pytaVSL.display_title("Chapitre 2 : L'idée lumineuse de Jack Caesar pour établir la paix publicitaire", 5),
            self.wait(5, 's'),
            pytaVSL.trijc_change_tool('aspi'),
            pytaVSL.animate('t_trijc_aspi', 'rotate_z', None, 0, 0.2, 's', 'elastic-inout'),
            pytaVSL.aspi_slide('m_layout', [0, -0.45], [0, 0.52], 0.6),
            pytaVSL.aspi_slide('m_ch2-3', [-0.02, -0.445], [-0.02, 0.53], 0.6),
            self.wait(1.2, 's'),
            pytaVSL.trijc_io('out', 'aspi', 0.4, 'elastic-inout'),
            self.wait(0.4, 's'),
            pytaVSL.trijc_io('in', 'tuba', 0.3, 'elastic-inout'),
            self.wait(0.3, 's'),

            # TODO manque un jingle ??
            self.f_ch2_4()
        ])

    @pedalboard_button(103)
    def f_ch2_4(self):
        self.start_scene('sequence/f_ch2_4', lambda: [
            pytaVSL.movie_in('f_ch2-4', 0.6),
            self.wait(5, 's'), # TODO affiner timing

        ])

    @pedalboard_button(104)
    def p_ch2_5(self):
        self.start_scene('sequence/p_ch2_5', lambda: [
            self.wait(5, 's'), # TODO affiner timing
            ###### TODO : déclencher fish au dernier moment ?

        ])



        ##### TODO voir si on met les scènes d'échec des Vanupiés
