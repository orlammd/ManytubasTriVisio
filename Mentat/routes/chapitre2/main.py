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
            # self.wait(0.2, 's'),

            # Chapitre 2
            self.m_ch2_1()
        ])

    def init_chapitre2(self):



        chapter = 'ch2'

        ### Création des groupes du chapitre
        # pytaVSL.create_group('tv_jc', ['plane_horn_jc', 'p_jc'])
        pytaVSL.create_group('tv1', ['plane_horn_1','p_' + chapter + '-5']) # Pub Paillassons
        pytaVSL.create_group('tv2', ['plane_horn_2', 'p_chaussure']) # Chaussure
        pytaVSL.create_group('tv3', ['plane_horn_3', 'p_pied']) # Pied

        pytaVSL.create_group('m_iraye', ['m_layout', 'm_' + chapter + '*'])
        pytaVSL.create_group('f_arabesques', ['f_arabesque_1', 'f_arabesque_2'])
        pytaVSL.create_group('f_arabesques_2', ['f_arabesque_3', 'f_arabesque_4'])
        pytaVSL.create_group('f_arabesques_3', ['f_arabesque_5', 'f_arabesque_6'])
        pytaVSL.create_group('f_ilm', ['f_arabesques', 'f_' + chapter + '*'])

        # Exceptions
        pytaVSL.create_group('f_ilm_up', ['f_arabesques_2', 'f_ch2-7_up'])
        pytaVSL.create_group('f_ilm_down', ['f_arabesques_3', 'f_ch2-7_down'])

        pytaVSL.sync()

        pytaVSL.position_overlay('Chapitre2')


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
        Jingle intempestif #2 (repoussé à la fin)
        """
        self.start_scene('sequence/jingle_intempestif_2', lambda: [
            pytaVSL.jc_jingle_io('top', 0.15, 'elastic-inout'), #### TODO à changer pour pouvoir pousser la fin
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
            self.wait(0.5, 's'),
            pytaVSL.animate('t_trijc_aspi', 'rotate_z', None, -10, 0.1, 's'),
            self.wait(0.1, 's'),
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
        """
        JC & Enedys dans le bureau
        """
        self.start_scene('sequence/f_ch2_4', lambda: [
            pytaVSL.movie_in('f_ch2-4', 0.6),
            self.wait(26.5, 's'), # TODO affiner timing
            pytaVSL.trijc_io('in', tool='compas', duration=1),
            self.wait(1.5, 's'),
            self.p_ch2_5(),
            self.wait(pytaVSL.get('f_ch2-4', 'video_end')- 26.5 -5 - 1.5 - 2, 's'),
            pytaVSL.set('sub_t_trijc_lustre_allume', 'alpha', 1),
            pytaVSL.trijc_io('in', 'lustre', duration=0.7),
            self.wait(0.7, 's'),
            pytaVSL.trijc_turn_lights('off', 1),
            pytaVSL.animate('f_ch2-4', 'alpha', None, 0, 1, 's'),
            pytaVSL.animate('f_arabesques', 'alpha', None, 0, 1, 's'),
            self.wait(1.1, 's'),
            pytaVSL.set('f*', 'visible', 0),
            pytaVSL.set('f*', 'alpha', 1),
            pytaVSL.trijc_change_tool('tuba'),
            pytaVSL.set('sub_t_trijc_lustre_allume', 'alpha', 1),
            self.wait(0.2, 's'),
            self.m_ch2_6()
        ])

    @pedalboard_button(104)
    def p_ch2_5(self):
        """
        Spot paillasson publicitaire
        """
        pytaVSL.shaking_tvs(1, 'p_ch2-5')
        pytaVSL.set('tv1', 'position_x', 1)
        pytaVSL.set('tv1', 'position_y', 0)
        pytaVSL.set('tv1', 'scale', 0.6, 0.6)
        pytaVSL.set('tv1', 'visible', 1)

        self.start_scene('sequence/p_ch2_5', lambda: [
            pytaVSL.animate('t_trijc_compas', 'rotate_z', None, -45, 0.1, 's', 'elastic-in-out'),
            self.wait(0.1, 's'),

            ###### TODO : déclencher fish au dernier moment ?

            pytaVSL.animate('t_trijc_compas', 'rotate_z', None, 0, 0.5, 's', 'elastic-inout'),
            pytaVSL.animate('f_ilm', 'scale', None, [0.4, 0.4], 0.5, 's'),
            pytaVSL.animate('f_ilm', 'position_x', None, -0.25, 0.5, 's', 'elastic-inout'),
            pytaVSL.animate('f_ilm', 'position_y', None, 0.25, 0.5, 's', 'elastic-inout'),
            pytaVSL.animate('tv1', 'position_x', None, 0.2, 0.5, 's', 'elastic-inout'),
            self.wait(0.5, 's'),
            pytaVSL.animate('tv1', 'scale', None, [0.8, 0.8], pytaVSL.get('p_ch2-5', 'video_end') - 0.5 - 1, 's'),
            pytaVSL.animate('tv1', 'position_x', None, 0.1, pytaVSL.get('p_ch2-5', 'video_end') - 0.5 - 1, 's'),
            pytaVSL.animate('t_trijc_compas', 'rotate_z', None, 20, pytaVSL.get('p_ch2-5', 'video_end') - 0.5 - 1, 's'),
            self.wait(pytaVSL.get('p_ch2-5', 'video_end') - 1, 's'), # TODO affiner timing
            # self.wait((pytaVSL.get('p_ch2-5', 'video_end') - 1) / 2 - 0.5, 's' ),
            pytaVSL.animate('tv1', 'scale', None, [0.6, 0.6], 0.5, 's', 'elastic-inout'),
            pytaVSL.animate('tv1', 'position_x', None, 0.2, 0.5, 's', 'elastic-inout'),
            pytaVSL.animate('t_trijc_compas', 'rotate_z', None, -45, 0.5, 's', 'elastic-inout'),
            self.wait(0.5, 's' ),
            pytaVSL.trijc_change_tool('aimant'),
            self.wait(0.1, 's'),
            pytaVSL.animate('t_trijc_aimant', 'rotate_z', None, -360, 0.5, 's', 'elastic-inout'),
            pytaVSL.animate('f_ilm', 'scale', None, [0.95, 0.95], 0.5, 's', 'elastic-inout'),
            pytaVSL.animate('f_ilm', 'position_x', None, 0, 0.5, 's', 'elastic-inout'),
            pytaVSL.animate('f_ilm', 'position_y', None, 0, 0.5, 's', 'elastic-inout'),
            pytaVSL.animate('tv1', 'position_x', None, 1, 0.5, 's', 'elastic-inout'),
            self.wait(0.5, 's'),
            pytaVSL.stop_animate('plane_horn_1', 'position'),
            pytaVSL.stop_animate('p_ch2-5', 'position'),
            pytaVSL.set('p_ch2-5', 'fish', 0),
            pytaVSL.trijc_io('out', 'aimant', 0.1, easing='elastic-inout')
        ])


    @pedalboard_button(105)
    def m_ch2_6(self):
        """
        Reprise narration Miraye
        """
        pytaVSL.miraye_in('m_ch2-6', 0.5)
        self.start_scene('sequence/m_ch2_6', lambda: [
            #### Attention au clash avec le lancement au pied du jingle
            self.wait(6.8, 's'),
            pytaVSL.animate('p_jc', 'rgbwave', 0, 1, 0.2, 's'),
            pytaVSL.animate('tv_jc', 'rgbwave', 0, 1, 0.2, 's'),
            self.wait(0.2, 's'),
            pytaVSL.animate('tv_jc', 'position_y', None, -1, 1, 's', 'random'),
            self.wait(1.2, 's'),
            pytaVSL.set('*jc', 'rgbwave', 0),
            pytaVSL.set('tv_jc', 'visible', 0),
            pytaVSL.stop_animate('plane_horn_jc', 'position_x'),
            pytaVSL.stop_animate('plane_horn_jc', 'position_y'),
            pytaVSL.stop_animate('p_jc', 'position_x'),
            pytaVSL.stop_animate('p_jc', 'position_y'),
            self.wait(pytaVSL.get('m_ch2-6', 'video_end') - 7 - 1.2 - 10, 's'),
            pytaVSL.animate('m_iraye', 'scale', None, [0.25, 0.25], 8, 's'),
            # pytaVSL.animate('m_iraye', 'position', None, [0.35, 0.15, pytaVSL.get('m_iraye', 'position_z')], 8, 's'),
            pytaVSL.animate('m_iraye', 'position_x', None, -0.2, 7, 's', 'exponential-inout'),
            pytaVSL.animate('m_iraye', 'position_y', None, 0.18, 7, 's'),
            self.wait(5, 's'),
            self.f_ch2_7()
        ])

    @pedalboard_button(3)
    def jingle_intempestif_3(self):
        pytaVSL.jc_jingle_in('bottom', 0.1, 'elastic-inout')


    @pedalboard_button(106)
    def f_ch2_7(self):
        """
        Enedys se rend au spectacle des Vanupiés
        """
        self.start_scene('sequence/f_ch2_7', lambda: [
            pytaVSL.movie_in('f_ch2-7', 0.7),
            self.wait(2, 's'),
            pytaVSL.animate('t_trijc_tuba', 'rotate_z', None, 7, 0.2, 's', 'elastic-inout'),
            pytaVSL.animate('m_iraye', 'position_x', None, 1, 1, 's', 'elastic-inout'),
            self.wait(0.3, 's'),
            pytaVSL.animate('t_trijc_tuba', 'rotate_z', None, 0, 0.5, 's', 'elastic-inout'),

            self.wait(117 - 2 - 0.3, 's'),
            self.dede_doah_chaussure()
        ])

    @pedalboard_button(107)
    def dede_doah_chaussure(self):
        """
        Doah rencontre Dédé qui lui demande d'enlever ses chaussures
        """
        self.start_scene('sequence/dede_doah_chaussure', lambda: [
            ### Idées de chaussures de Doah
            pytaVSL.set('tv2', 'visible', 1),
            pytaVSL.set('tv3', 'visible', 1),
            pytaVSL.shaking_tvs(2, 'p_pied'),
            pytaVSL.shaking_tvs(3, 'p_chaussure'),
            pytaVSL.animate('tv2', 'position_x', None, -0, 1, 's'),
            pytaVSL.animate('tv3', 'position_x', None, 0, 1, 's'),
            self.wait(3, 's'),
            pytaVSL.animate('tv2', 'position_y', None, 1, 0.2, 's', 'elastic-inout'),
            pytaVSL.animate('tv3', 'position_y', None, 1, 0.2, 's', 'elastic-inout'),
            self.wait(0.4, 's'),
            pytaVSL.set('tv2', 'visible', 0),
            pytaVSL.set('tv3', 'visible', 0),
            pytaVSL.stop_animate('plane_horn*', 'position_x'),
            pytaVSL.stop_animate('plane_horn*', 'position_y'),
            pytaVSL.stop_animate('p_pied', 'position_x'),
            pytaVSL.stop_animate('p_pied', 'position_y'),
            pytaVSL.stop_animate('p_chaussure', 'position_x'),
            pytaVSL.stop_animate('p_chaussure', 'position_y'),

            #### Fin de la séquence /// Arrivée et tombée Panneau entracte
            self.wait(208 - 2 - 0.3 -117 - 3 - 0.4, 's'),
            self.proposition_entracte()
        ])

    @pedalboard_button(108)
    def button_proposition_entracte(self):
        self.stop_scene('sequence/*')
        self.proposition_entracte()

    def proposition_entracte(self):
        pytaVSL.set('f_ch2-7_up', 'video_time', 209) # A enlever
        pytaVSL.set('f_ch2-7_down', 'video_time', 212) # A enlever

        self.start_scene('sequence/proposition_entracte', lambda: [
            pytaVSL.set('f_ch2-7', 'video_speed', 0),
            pytaVSL.set('sub_t_trijc_lustre_allume', 'alpha', 1),
            pytaVSL.trijc_io('in', 'lustre', 0.6, 'elastic-inout'),
            self.wait(0.65, 's'),
            pytaVSL.trijc_turn_lights('off', 1),
            pytaVSL.animate('f_arabesque_1', 'alpha', None, 0, 1, 's'),
            pytaVSL.animate('f_arabesque_2', 'alpha', None, 0, 1, 's'),
            pytaVSL.animate('f_ch2-7', 'alpha', None, 0, 1, 's'),

            pytaVSL.set('f_ilm_up', 'visible', 1),
            pytaVSL.set('f_ch2-7_up', 'visible', 1),
            pytaVSL.set('f_ch2-7_up', 'video_speed', 1),            #####" A enelever
            pytaVSL.set('f_ilm_down', 'visible', 1),


            #### TODO : préciser ce qui suit avec les films bien découpés.
            pytaVSL.animate('f_ilm_up', 'position_y', None, 0.25, 1, 's', 'elastic-inout'),
            pytaVSL.animate('lights*', 'alpha', None, 1, 3, 's'),
            self.wait(3, 's'),

            pytaVSL.set('f_ilm', 'visible', 0),
            pytaVSL.set('f_ch2-7', 'visible', 0),
            pytaVSL.set('f_arabesque_1', 'alpha', 1),
            pytaVSL.set('f_arabesque_2', 'alpha', 1),
            pytaVSL.set('f_ch2-7', 'alpha', 1),


            #### OPTIONNEL : les panneaux se croisent
            self.wait(0.1,'s'),
            #### Fin OPTIONNEL
            pytaVSL.set('f_ch2-7_down', 'visible', 1),
            pytaVSL.set('f_ch2-7_down', 'video_speed', 1),                        ##### A enelever
            pytaVSL.animate('f_ilm_down', 'position_y', None, -0.25, 1, 's', 'elastic-inout'),
            self.wait(7, 's'), #### TODO à caler en conction des vrais films
            pytaVSL.animate('f_ilm_up', 'position_y', None, -0.71, 0.4, 's', 'elastic-inout'),
            self.wait(0.4, 's'),
            pytaVSL.set('f_ilm_up', 'visible', 0),
            pytaVSL.animate('f_ilm_down', 'scale', None, [0.95, 0.95], 1, 's', 'elastic-out'),
            pytaVSL.animate('f_ilm_down', 'position_y', None, 0, 1, 's', 'elastic-out'),
            pytaVSL.animate('f_ilm_down', 'position_x', None, 0, 1, 's', 'elastic-out')
        ])

    @pedalboard_button(4)
    def m_ch2_8(self):
        """
        Miraye - On enchaîne là
        """
        self.start_scene('m_ch2_8', lambda: [
            pytaVSL.trijc_change_tool('tuba'),
            self.wait(0.1, 's'),
            pytaVSL.miraye_in('m_ch2-8'),
            self.wait(1, 's'),
            pytaVSL.animate('f_ilm_down', 'rgbwave', None, 0.6, 0.8, 's', 'exponential-out'),
            self.wait(0.2, 's'),
            # pytaVSL.animate('f_ilm_down', 'position_x', None, 0, 0.5, 's', 'elastic-inout'),
            self.wait(pytaVSL.get('m_ch2-8', 'video_end') - 0.2 - 0.5 - 0.8, 's'),
            pytaVSL.trijc_change_tool('aspi'),
            self.wait(0.1, 's'),
            pytaVSL.animate('t_trijc_aspi', 'rotate_z', None, 0, 0.2, 's', 'elastic'),
            pytaVSL.aspi_slide('m_layout', [0, -0.45], [0, 0.52], 0.6),
            pytaVSL.aspi_slide('m_ch2-8', [-0.02, -0.445], [-0.02, 0.53], 0.6),
            self.wait(0.6, 's'),
            pytaVSL.trijc_io('out', 'aspi', 0.5),
            pytaVSL.animate('lights*', 'alpha', None, 0.3, 1, 's'),
            self.f_ch2_9()
        ])

    @pedalboard_button(109)
    def f_ch2_9(self):
        """
        Numéro de Dagz
        """
        pytaVSL.set('f_ch2-9', 'rgbwave', 0.5)
        pytaVSL.set('f_ch2-9', 'visible', 1)
        pytaVSL.set('f_ilm', 'visible', 1)
        pytaVSL.animate('f_ch2-9', 'rgbwave', 0.5, 0, 0.5, 's')
        pytaVSL.set('f_ilm_down', 'visible', 0),

    @pedalboard_button(5)
    def f_ch2_10(self):
        """
        Explosion + fin Dédé
        """
        self.start_scene('f_ch2-10', lambda: [
            pytaVSL.f_noisy_switch_video('f_ch2-9', 'f_ch2-10', 0.5),
            self.wait(3, 's'), # Affiner avec la vidéo
            # pytaVSL.set('f_arabesque_1', 'position_y', 2.35),
            # pytaVSL.set('f_arabesque_2', 'position_y', -1.47),
            # self.wait('')
            self.wait(pytaVSL.get('f_ch2-10', 'video_end') - 3, 's'),
            engine.set_route('Chapitre 3')
        ])

    @pedalboard_button(6)
    def jingle_jc_enedys(self):
        """
        Jingle pendant discours Enedys
        """
        pytaVSL.jc_jingle_io('top', 0.3, 'elastic-inout')
