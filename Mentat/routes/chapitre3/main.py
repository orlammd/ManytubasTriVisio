from ..base import RouteBase, pedalboard_button
from .video import Video
from .light import Light

from modules import *

class Chapitre3(Video, Light, RouteBase):

    def activate(self):
        """
        Called when the engine switches to this route.
        """

        super().activate()

        transport.set_tempo(60)
        transport.set_cycle('4/4', pattern="Xxxx")

        # Setups, banks...
        prodSampler.set_kit(self.name)

        self.start_scene('init_chapitre3', lambda: [
            # Overlay
            self.init_chapitre3(),

            # Chapitre 3
            self.m_ch3_1()
        ])

    def init_chapitre3(self):



        chapter = 'ch3'

        ### Création des groupes du chapitre
        pytaVSL.create_group('tv1', ['plane_horn_1','p_' + chapter + '-3']) # Soft & Rains dans le journal

        pytaVSL.create_group('m_iraye', ['m_layout', 'm_' + chapter + '*'])
        pytaVSL.create_group('f_arabesques', ['f_arabesque_1', 'f_arabesque_2'])
        pytaVSL.create_group('f_arabesques_2', ['f_arabesque_3', 'f_arabesque_4'])
        pytaVSL.create_group('f_arabesques_3', ['f_arabesque_5', 'f_arabesque_6'])
        pytaVSL.create_group('f_ilm', ['f_arabesques', 'f_' + chapter + '*'])

        pytaVSL.sync()

        pytaVSL.position_overlay('Chapitre3')


    @pedalboard_button(100)
    def m_ch3_1(self):
        """
        Intro Miraye
        """
        self.start_scene('sequence/m_ch3_1', lambda: [
            pytaVSL.trijc_io('in', 'tuba', 1),
            self.wait(1, 's'),
            pytaVSL.miraye_in('m_ch3-1'),
            self.wait(pytaVSL.get('m_ch3-1', 'video_end') - 1),
            pytaVSL.trijc_change_tool('aspi'),
            self.wait(0.2, 's'),
            pytaVSL.animate('t_trijc_aspi', 'rotate_z', None, 0, 0.2, 's', 'elastic-inout'),
            self.wait(0.1, 's'),
            pytaVSL.aspi_slide('m_layout', [0, -0.45], [0, 0.52], 0.6),
            pytaVSL.aspi_slide('m_ch3-1', [-0.02, -0.445], [-0.02, 0.53], 0.6),
            self.wait(0.8, 's'),
            self.f_ch3_2()
        ])

    @pedalboard_button(101)
    def f_ch3_2(self):
        """
        Enedys recrute Soft & Rains
        """
        self.start_scene('sequence/f_ch3_2', lambda: [
            pytaVSL.trijc_change_tool('tuba'),
            self.wait(0.2, 's'),
            pytaVSL.movie_in('f_ch3-2', 0.5),
            self.wait(25.5, 's'),
            self.p_ch3_3(),
            self.wait(pytaVSL.get('f_ch3-2', 'video_end') - 25.5, 's'),
            self.f_ch3_4()
        ])

    @pedalboard_button(102)
    def p_ch3_3(self):
        """
        Journal passe à la télé
        """
        self.start_scene('sequence/pch3_3', lambda: [
            pytaVSL.set('tv1', 'visible', 1),
            pytaVSL.shaking_tvs(1, 'p_ch3-3'),
            pytaVSL.set('p_ch3-3', 'video_time', 26), # TODO à enlever
            pytaVSL.animate('tv1', 'position_x', None, 0.2, 0.5, 's', 'elastic-inout'),
            self.wait(0.5, 's'),
            pytaVSL.animate('tv1', 'position_x', None, -0.1, 3, 's'),
            self.wait(3, 's'),
            pytaVSL.animate('tv1', 'position_x', None, -0.7, 0.5, 's', 'elastic-inout'),
            self.wait(1, 's'),
            pytaVSL.stop_animate('plane_horn_1', 'position_x'),
            pytaVSL.stop_animate('plane_horn_1', 'position_y'),
            pytaVSL.stop_animate('p_ch3-3', 'position_x'),
            pytaVSL.stop_animate('p_ch3-3', 'position_y'),
            pytaVSL.set('p_ch3-3', 'fish', 0)
        ])

    @pedalboard_button(103)
    def f_ch3_4(self):
        """
        Les Barons déambulent -> Saladin veut jouer du violon
        """
        self.start_scene('sequence/f_ch3_4', lambda: [
            pytaVSL.f_switch_video('f_ch3-2', 'f_ch3-4'),
            self.wait(12.3, 's'),
            self.m_ch3_5()
        ])

    @pedalboard_button(104)
    def m_ch3_5(self):
        """
        Miraye hurle contre le violon et propose des crêpes
        """
        self.start_scene('sequence/m_ch3_5', lambda: [
            pytaVSL.trijc_io('in', 'tuba', 0.2, 'random'),
            pytaVSL.animate('f_ch3-4', 'rgbwave', None, 0.3, 1, 's'),
            self.wait(0.2, 's'),
            pytaVSL.miraye_in('m_ch3-5', 0.3),
            self.wait(0.5, 's'),
            pytaVSL.set('f_ch3-4', 'video_speed', 0),
            self.wait(0.3, 's'),
            self.wait(pytaVSL.get('m_ch3-5', 'video_end') - 0.3 - 1, 's'),
            pytaVSL.trijc_change_tool('aspi'),
            self.wait(0.8, 's'),
            pytaVSL.animate('t_trijc_aspi', 'rotate_z', None, 0, 0.2, 's', 'elastic-inout'),
            pytaVSL.aspi_slide('m_layout', [0, -0.45], [0, 0.52], 0.3),
            pytaVSL.aspi_slide('m_ch3-5', [-0.02, -0.445], [-0.02, 0.53], 0.3),
            pytaVSL.trijc_io('out', 'aspi'),
            self.f_ch3_6()
        ])

    @pedalboard_button(105)
    def f_ch3_6(self):
        """
        Les Barons ont du matos à crêpes
        """
        self.start_scene('sequence/f_ch3_6', lambda: [
            pytaVSL.set('f_ch3-6', 'rgbwave', 0.3),
            pytaVSL.set('f_ch3-6', 'visible', 1),
            pytaVSL.set('f_ch3-4', 'visible', 0),
            pytaVSL.set('f_ch3-4', 'rgbwave', 0),
            pytaVSL.animate('f_ch3-6', 'rgbwave', None, 0, 1, 's'),
            # pytaVSL.set('f_ch3-6', 'video_speed', 1),
            #### TODO vanupié récupération de la poele et tout
            self.wait(pytaVSL.get('f_ch3-6', 'video_end'), 's'),
            pytaVSL.f_switch_video('f_ch3-6', 'f_ch3-6_waiting'),
            self.m_ch3_7()
        ])

    @pedalboard_button(106)
    def m_ch3_7(self):
        """
        Miraye demande d'enchaîner
        """
        self.start_scene('sequence/m_ch3-7', lambda: [
            pytaVSL.trijc_io('in', 'tuba', 0.5),
            self.wait(0.5, 's'),
            pytaVSL.miraye_in('m_ch3-7', 0.3),
            self.wait(0.5, 's'),
            pytaVSL.trijc_change_tool('aspi'),
            self.wait(pytaVSL.get('m_ch3-7', 'video_end') - 0.7, 's'),
            pytaVSL.animate('t_trijc_aspi', 'rotate_z', None, 0, 0.2, 's', 'elastic-inout'),
            pytaVSL.aspi_slide('m_layout', [0, -0.45], [0, 0.52], 0.3),
            pytaVSL.aspi_slide('m_ch3-7', [-0.02, -0.445], [-0.02, 0.53], 0.3),
            self.wait(0.7, 's'),
            pytaVSL.trijc_change_tool('lustre'),
            pytaVSL.trijc_turn_lights('off', 0.5),
            pytaVSL.animate('f_ch3-6_waiting', 'alpha', None, 0, 0.5),
            self.wait(0.5, 's'),
            self.f_ch3_8()
        ])

    @pedalboard_button(107)
    def f_ch3_8(self):
        """
        S&R chez le Fakir
        """
        self.start_scene('sequence/f_ch3_8', lambda: [
            pytaVSL.set('f_ch3-8', 'visible', 1),
            pytaVSL.trijc_turn_lights('on', 0.5),
            pytaVSL.set('f_ch3-6_waiting', 'visible', 0),
            pytaVSL.animate('f_ch3-8', 'alpha', None, 1, 0.5),
            self.wait(0.5, 's'),
            pytaVSL.trijc_io('out', 'lustre'),
            self.wait(pytaVSL.get('f_ch3-8', 'video_end') - 0.5, 's'),
            self.f_ch3_9()
        ])

    @pedalboard_button(108)
    def f_ch3_9(self):
        """
        Dagz essaie le cerceau
        """
        self.start_scene('sequence/f_ch3_9', lambda: [
            pytaVSL.f_switch_video('f_ch3-8', 'f_ch3-9'),
        ])

    @pedalboard_button(1)
    def f_ch3_10(self):
        """
        La spatule arrive sur le paillasson du fakir
        """
        self.start_scene('sequence/f_ch3_10', lambda: [
            pytaVSL.f_switch_video('f_ch3-9', 'f_ch3-10'),
            self.wait(pytaVSL.get('f_ch3-10', 'video_end'), 's'),
            self.f_ch3_11()
        ])

    @pedalboard_button(110)
    def f_ch3_11(self):
        """
        Soft & Rains et la voyante
        """
        self.start_scene('sequence/f_ch3_11', lambda: [
            pytaVSL.f_switch_video('f_ch3-10', 'f_ch3-11'),
        ])

    @pedalboard_button(2)
    def f_ch3_12(self):
        """
        La crêpe arrive sur la boule de cristal
        """
        self.start_scene('sequence/f_ch3_12', lambda: [
            pytaVSL.f_switch_video('f_ch3-11', 'f_ch3-12'),
            self.wait(pytaVSL.get('f_ch3-12', 'video_end'), 's'),
            self.f_ch3_13()
        ])

    @pedalboard_button(111)
    def f_ch3_13(self):
        """
        Soft & Rains cez Dalida
        """
        self.start_scene('sequence/f_ch3_13', lambda: [
            pytaVSL.f_switch_video('f_ch3-12', 'f_ch3-13'),
            self.wait(pytaVSL.get('f_ch3-13', 'video_end'), 's'),
            pytaVSL.f_switch_video('f_ch3-13', 'f_ch3-13_waiting')
        ])

    @pedalboard_button(3)
    def f_ch3_14(self):
        """
        La poële arrive sur la tête de S&R
        """
        self.start_scene('sequence/f_ch3_14', lambda: [
            pytaVSL.f_switch_video('f_ch3-13_waiting', 'f_ch3-14'),
            self.wait(pytaVSL.get('f_ch3-14', 'video_end')-5, 's'),
            pytaVSL.trijc_io('in', 'lustre', 3),
            self.wait(2, 's'),
            pytaVSL.trijc_turn_lights('off', 2),
            pytaVSL.animate('f_*', 'alpha', None, 0, 2),
            self.wait(5, 's'),
            pytaVSL.set('f_ilm', 'visible', 0),
            pytaVSL.set('f_*', 'alpha', 1),
            engine.set_route('Chapitre 4')
        ])
