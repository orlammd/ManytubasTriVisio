from ..base import RouteBase, pedalboard_button
from .video import Video
from .light import Light
from random import random as _rand

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


        self.start_scene('init_chapitre1', lambda: [
            # Overlay
            self.init_pyta(),
            self.wait(0.2, 's'),

            # Chapitre 1
            self.lancement_miraye_1()
        ])

    def init_pyta(self):
        # Degroupage des TV
        #### A priori inutile ?

        # Reset des slides
        pytaVSL.reset()

        def create_tv_groups():
            for index in range(1,5):
                pytaVSL.create_group('tv' + str(index), ['plane_horn_' + str(index), ',p_ch1-' + str(index+2)])

        chapter = 'ch1'
        self.start_scene('groups_and_overlay', lambda: [
            # Chargement de l'overlay commun
            pytaVSL.position_overlay('Common'),

            ### Création des groupes du chapitre
            pytaVSL.create_group('m_iraye', ['m_layout', 'm_' + chapter + '*']),
            pytaVSL.create_group('f_arabesques', ['f_arabesque*']),
            self.wait(0.1, 's'),
            pytaVSL.create_group('f_ilm', ['f_arabesques', 'f_ch1-*']),
            create_tv_groups(),
            pytaVSL.check_new_slides(once=True),
            self.wait(0.1, 's'),
            pytaVSL.position_overlay('Chapitre1'),

        ])

    @pedalboard_button(1)
    def lancement_miraye_1(self):
        """
        Lancement Miraye Part 1
        """
        self.start_scene('sequence/lancement_miraye_1', lambda: [
            ### Lancement du Film
            pytaVSL.trijc_io('in', 'tuba', 1, 'elastic-inout'),
            self.wait(1.2, 's'),
            pytaVSL.miraye_in('m_ch1-1', 1)
            ]
        )

    @pedalboard_button(2)
    def m_ch1_2(self):
        """
        Intro
        """

        self.start_scene('sequence/m_ch1-2', lambda: [
            pytaVSL.trijc_change_tool('compas'),
            pytaVSL.m_noisy_switch_video('m_ch1-1', 'm_ch1-2', 0.5),
            self.wait(pytaVSL.get('m_ch1-2', 'video_end'), 's'),
            self.actes_jc(),
            ]
        )

    @pedalboard_button(100)
    def actes_jc(self):
        """
        Les actes de JC
        """

        for index in range(1,5):
            pytaVSL.shaking_tvs(index, 'p_ch1-' + str(index + 2))

        self.start_scene('sequence/actes_jc', lambda:[
            pytaVSL.m_noisy_switch_video('m_ch1-2', 'm_ch1-2_waiting', 5),
            pytaVSL.animate('m_iraye', 'scale', None, [0.26, 0.26], 2, 's', 'random'),
            pytaVSL.animate('t_trijc_compas', 'rotate_z', None, 45, 1, 's', 'random'), # à remplacer par des mvts de ciseaux
            self.wait(1, 's'),
            pytaVSL.animate('t_trijc_compas', 'rotate_z', None, 0, 1, 's', 'random'), # à remplacer par des mvts de ciseaux
            pytaVSL.wait(1, 's'),
            pytaVSL.trijc_change_tool('aimant'),
            pytaVSL.wait(0.2, 's'),
            pytaVSL.animate('t_trijc_aimant', 'rotate_z', None, -40, 0.5, 's', 'elastic-inout'),
            pytaVSL.animate('t_trijc_aimant', 'rotate_z', None, -90, 1.5, 's', 'elastic-inout'),
            pytaVSL.animate('m_iraye', 'position_y', None, -0.35, 1.5, 's', 'elastic-inout'),
            self.wait(1.5, 's'),
            pytaVSL.animate('t_trijc_aimant', 'rotate_z', None, 0, 1, 's'),

            pytaVSL.set('tv1', 'visible', 1.0),
            pytaVSL.set('p_ch1-3', 'video_time', 0),
            pytaVSL.animate('tv1', 'position_x', None, 0.09, 2, 's'),
            self.wait(3, 's'),
            pytaVSL.animate('tv1', 'position_x', None, -1, 2, 's'),
            pytaVSL.set('tv2', 'visible', 1.0),
            pytaVSL.set('p_ch1-4', 'video_time', 0),
            pytaVSL.animate('tv2', 'position_x', None, 0.09, 2, 's'),
            self.wait(3, 's'),
            pytaVSL.animate('tv2', 'position_x', None, -1, 2, 's'),
            pytaVSL.set('tv3', 'visible', 1.0),
            pytaVSL.set('p_ch1-5', 'video_time', 0),
            pytaVSL.animate('tv3', 'position_x', None, 0.09, 2, 's'),
            self.wait(3, 's'),
            pytaVSL.animate('tv3', 'position_x', None, -1, 2, 's'),
            pytaVSL.set('tv4', 'visible', 1.0),
            pytaVSL.set('p_ch1-6', 'video_time', 0),
            pytaVSL.animate('tv4', 'position_x', None, 0.09, 2, 's'),
            self.wait(3, 's'),
            pytaVSL.animate('tv4', 'position_x', None, -1, 2, 's'),
            self.wait(2, 's'),
            pytaVSL.set('tv*', 'visible', 0),
            pytaVSL.stop_animate('plane_horn*', 'position_x'),
            pytaVSL.stop_animate('plane_horn*', 'position_y'),
            pytaVSL.stop_animate('p_ch1-*', 'position_x'),
            pytaVSL.stop_animate('p_ch1-*', 'position_y'),
            self.m_ch1_7()
            ])

    @pedalboard_button(101)
    def m_ch1_7(self):
        """
        Poursuite de l'intro
        """
        self.start_scene('sequence/m_ch1_7', lambda:[
            pytaVSL.m_noisy_switch_video('m_ch1-2_waiting', 'm_ch1-7', 7),
            pytaVSL.animate('t_trijc_aimant', 'rotate_z', None, -90, 0.5, 's'),
            self.wait(0.5, 's'),
            pytaVSL.animate('t_trijc_aimant', 'rotate_z', None, -40, 1.5, 's', 'elastic-inout'),
            pytaVSL.animate('m_iraye', 'position_y', None, 0.016, 1.5, 's', 'elastic-inout'),
            self.wait(1.5, 's'),
            pytaVSL.trijc_change_tool('compas'),
            self.wait(0.2, 's'),
            pytaVSL.animate('m_iraye', 'scale', None, [0.837, 0.837], 1, 's', 'random'),
            pytaVSL.animate('t_trijc_compas', 'rotate_z', None, -45, 0.5, 's', 'random'), # à remplacer par des mvts de ciseaux
            self.wait(1, 's'),
            pytaVSL.animate('t_trijc_compas', 'rotate_z', None, 0, 0.5, 's', 'random'), # à remplacer par des mvts de ciseaux
            self.wait(50, 's'),
            pytaVSL.m_noisy_switch_video('m_ch1-7', 'm_ch1-7_waiting', 0.1)
        ])

    @pedalboard_button(3)
    def m_ch1_8(self):
        """
        Suite intro
        """
        self.start_scene('sequence/m_ch1_8', lambda:[
            pytaVSL.m_noisy_switch_video('m_ch1-7_waiting', 'm_ch1-8', 0.1),
        ])


    @pedalboard_button(4)
    def jack_casear_jingle(self):
        """
        Lancement du jingle Jack Caesar
        """

        pytaVSL.shaking_tvs(1, 'p_ch1-3')

        self.start_scene('sequence/jack_caesar_jingle', lambda: [
            pytaVSL.set('tv1', 'visible', 1),
            pytaVSL.set('tv1', 'position_z', -12),
            pytaVSL.animate('tv1', 'position_x', None, 0.09, 0.3, 's', 'elastic-inout'),
            pytaVSL.animate('tv1', 'position_y', None, 0.01, 0.15, 's', 'random'),
            self.wait(0.15, 's'),
            pytaVSL.animate('tv1', 'position_y', None, 0.0, 0.15, 's', 'random'),
            self.wait(pytaVSL.get('p_ch1-3', 'video_end') - 0.15, 's'),
            pytaVSL.animate('tv1', 'position_x', None, 1, 0.3, 's', 'exponential-inout'),
            pytaVSL.animate('tv1', 'position_y', None, 0.01, 0.15, 's', 'random'),
            self.wait(0.15, 's'),
            pytaVSL.animate('tv1', 'position_y', None, 0.0, 0.15, 's', 'random'),
            self.wait(0.15, 's'),
            pytaVSL.stop_animate('plane_horn_1', 'position_x'),
            pytaVSL.stop_animate('plane_horn_1', 'position_y'),
            pytaVSL.stop_animate('p_ch1-3', 'position_x'),
            pytaVSL.stop_animate('p_ch1-3', 'position_y'),
            pytaVSL.trijc_change_tool('aspi'),
            self.wait(0.2, 's'),
            pytaVSL.animate('t_trijc_aspi', 'rotate_z', None, -5, 0.5, 's', ),
            self.wait(0.5, 's'),
            self.f_ch1_9()
        ])

    @pedalboard_button(102)
    def f_ch1_9(self):
        """
        Bobine de Fin
        """
        self.start_scene('sequence/f_ch1_9', lambda: [
            pytaVSL.animate('t_trijc_aspi', 'rotate_z', None, 0, 0.2, 's', 'elastic'),
            pytaVSL.aspi_slide('m_layout', [0, -0.45], [0, 0.52], 0.6),
            pytaVSL.aspi_slide('m_ch1-8', [-0.02, -0.445], [-0.02, 0.53], 0.6),
            self.wait(1.2, 's'),
            pytaVSL.trijc_io('out', 'aspi', 0.7, 'elastic-inout'),
            self.wait(0.8, 's'),
            pytaVSL.trijc_io('in', 'tuba', 0.6, 'elastic-inout'),
            self.wait(0.7, 's'),
            pytaVSL.movie_in('f_ch1-9', 0.6),
            self.wait(pytaVSL.get('f_ch1-9', 'video_end') - 0.6, 's'),
            self.m_ch1_10()
        ])

    @pedalboard_button(103)
    def m_ch1_10(self):
        """
        Intervention Miraye
        """
        self.start_scene('sequence/m_ch1_10', lambda: [
            pytaVSL.signs_io('in', duration=0.5, easing='random'),
            pytaVSL.animate('lights*', 'alpha', None, 1, 0.5, 's',  'random'),
            pytaVSL.trijc_io('in', 'tuba', 0.5, 'random'),
            pytaVSL.shaking_slide('f_ch1-9', 'position_x', (_rand() / 2 + 0.5) * 0.01, 10),
            pytaVSL.shaking_slide('f_ch1-9', 'position_y', _rand() * 0.01, 5, easing='random'),
            self.wait(0.4, 's'),
            pytaVSL.trijc_change_tool('compas'),
            pytaVSL.miraye_in('m_ch1-10', 0.5),
            pytaVSL.set('f_ch1-9', 'video_speed', 0),
            pytaVSL.animate('t_trijc_compas', 'rotate_z', None, 10, 0.5, 's'),
            self.wait(0.5, 's'),
            pytaVSL.trijc_change_tool('aimant'),
            pytaVSL.animate('t_trijc_aimant', 'rotate_z', None, -45, 0.5, 's'),
            pytaVSL.animate('f_ilm', 'scale', None, [0.6, 0.6], 0.2, 's', 'elastic-inout'),
            self.wait(0.2, 's'),
            pytaVSL.animate('f_ilm', 'scale', None, [0.3, 0.3], 1, 's'),
            pytaVSL.animate('f_ilm', 'position_x', None, -0.35, 1, 's'),
            pytaVSL.animate('f_ilm', 'position_y', None, 0.15, 1, 's'),
            self.wait(0.5, 's'),
            pytaVSL.trijc_change_tool('compas'),
            self.wait(0.5, 's'),
            pytaVSL.animate('t_trijc_compas', 'rotate_z', None, -40, 13, 's'),
            pytaVSL.animate('m_iraye', 'scale', None, [0.5, 0.5], 13, 's'),
            pytaVSL.animate('m_iraye', 'position_x', None, 0.1, 13, 's'),
            self.wait(15, 's'), # TODO Séparer en deux vidéos ?
            pytaVSL.display_title('Chapitre 1 : Préambule', 3),
            self.wait(10, 's'), # TODO A affiner - moment où elle commence à raconter l'histoire
            self.f_ch1_11()
        ])

    @pedalboard_button(104)
    def f_ch1_11(self):
        self.start_scene('sequence/f_ch1_11', lambda: [
            pytaVSL.f_noisy_switch_video('f_ch1-9', 'f_ch1-11', 1),
            pytaVSL.animate('m_iraye', 'scale', None, [0.3, 0.3], 8, 's'),
            pytaVSL.animate('f_ilm', 'scale', None, [0.95, 0.95], 8, 's'),
            pytaVSL.animate('m_iraye', 'position', None, [0.35, 0.15, pytaVSL.get('m_iraye', 'position_z')], 8, 's'),
            pytaVSL.animate('f_ilm', 'position', None, [0, 0, pytaVSL.get('f_ilm', 'position_z')], 8, 's'),
            pytaVSL.stop_animate('f_ch1-9', 'position_x'), #, None, 0, 8, 's'),
            pytaVSL.stop_animate('f_ch1-9', 'position_y'), #, None, 0, 8, 's', 'random'),
            ## TODO Tout ce qui suit à synchroniser avec le film
            self.wait(8, 's'),
            pytaVSL.trijc_change_tool('lustre'),
            self.wait(0.3, 's'),
            pytaVSL.trijc_turn_lights('off', 1),
            pytaVSL.animate('m_layout', 'alpha', None, 0, 1, 's'),
            pytaVSL.animate('m_ch1-10', 'alpha', None, 0, 1, 's'),
            pytaVSL.animate('lights*', 'alpha', None, 0.3, 1, 's'),
            self.wait(2, 's'),
            pytaVSL.trijc_io('out', 'lustre', 2),
            self.wait(1, 's'),
            pytaVSL.signs_io('out', duration=1, easing='elastic-inout'),
        ])

    @pedalboard_button(5)
    def hb_instruments_direction(self):
        self.start_scene('sequence/hb_instruments_direction', lambda: [
            pytaVSL.v_hackboat_io('in'),
            #### Scènes des instruments de direction
            self.wait(1, 's'),
            self.f_ch1_12()
        ])

    @pedalboard_button(105)
    def f_ch1_12(self):
        """
        Les BF se promènent
        """
        self.start_scene('sequence/f_ch1_12', lambda: [
            pytaVSL.f_switch_video('f_ch1-11', 'f_ch1-12'),
        ])


    @pedalboard_button(6)
    def f_ch1_13(self):
        """
        Saladin approche / bruit au plateau
        """
        self.start_scene('f_ch1_13', lambda: [
            pytaVSL.f_noisy_switch_video('f_ch1-12', 'f_ch1-13'),
        ])

    @pedalboard_button(7)
    def f_ch1_14(self):
        """
        Allumage lumières
        """
        self.start_scene('sequence/f_ch1_14', lambda: [
            pytaVSL.animate('lights*', 'alpha', None, 1, 0.2, 's'),
            pytaVSL.f_switch_video('f_ch1-13', 'f_ch1-14'),
            self.wait(3, 's'),
            pytaVSL.animate('lights*', 'alpha', None, 0.2, 5, 's'),
            self.wait(pytaVSL.get('f_ch1-14', 'video_end')),
            self.f_ch1_15()
        ])

    @pedalboard_button(106)
    def f_ch1_15(self):
        """
        Doah chez la voyante
        """
        self.start_scene('sequence/f_ch1_15', lambda: [
            pytaVSL.f_switch_video('f_ch1-14', 'f_ch-15'),
            self.wait(pytaVSL.get('f_ch1-15', 'video_end')),
            self.f_ch1_16()
        ])

    @pedalboard_button(106)
    def f_ch1_16(self):
        """
        Musée zarbi de l'étrange
        """
        self.start_scene('sequence/f_ch1_16', lambda: [
            pytaVSL.f_switch_video('f_ch1-15', 'f_ch-16'),
            self.wait(pytaVSL.get('f_ch1-16', 'video_end') - 10), # TODO à affiner en fonction de la fin du film
            pytaVSL.trijc_io('in', 'lustre', 7),
            pytaVSL.trijc_turnlights('off', 3),
            pytaVSL.animate('f_*', 'alpha', None, 0, 3),
            self.wait(3.2, 's'),
            pytaVSL.set('f_ilm', 'visible', 0),
            pytaVSL.set('f_*', 'alpha', 1),
            self.engine.set_route('Chapitre 2')
        ])

# TODO A virer à la fin
    @pedalboard_button(10000)
    def m_titre(self):
        pytaVSL.display_title('Chapitre 1 : Preambule', 3)

    @pedalboard_button(999)
    def utilise_un_lustre(self):
        pytaVSL.trijc_change_tool('lustre')

    @pedalboard_button(1000)
    def baisse_light(self):
        pytaVSL.trijc_turn_lights('off', 1)
