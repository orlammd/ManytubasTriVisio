from ..base import RouteBase, pedalboard_button
from .video import Video
from .light import Light
import time
from random import random as _rand

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

        self.start_scene('activate_pyta', self.activate_pyta)


    def activate_pyta(self):
        ### Load slides
        pytaVSL.load_slides_from_dir('Common')
        pytaVSL.load_slides_from_dir('Chapitre1')
        while not pytaVSL.get('ready'):
            self.wait(0.1, 's')

        ### Create clones
        for clone_name in [
            'signs_standright_jack',
            'signs_standright_caesar',
            'signs_standleft_caesar',
            'signs_standright_manytubas',
            'signs_standleft_manytubas',
            'signs_standcenter_manytubas',
            'signs_standright_tri',
            'signs_standleft_tri',
            'signs_standright_visio',
            'signs_standleft_visio']:
            pytaVSL.create_clone('signs_standleft_jack', clone_name)

        for clone_name in [
            'plane_horn_5',
            'plane_horn_4',
            'plane_horn_3',
            'plane_horn_2']:
            pytaVSL.create_clone('plane_horn_1', clone_name)

        ### Create groups
        for slides_group in [
            'trijc',
            't_trijc',
            'ot_trijc',
            'lights',
            ]:
            pytaVSL.create_group(slides_group, [slides_group + '*'])
        # pytaVSL.create_group('w_trijc', ['trijc', 't_trijc', 'ot_trijc'])
        for slides_group in [
            'jack',
            'caesar',
            'manytubas',
            'tri',
            'visio',
            ]:
            pytaVSL.create_group('w_signs_' + slides_group, ['signs*' + slides_group])
        # pytaVSL.create_group('w_signs', ['w_signs_*'])

        for index in range(1,6):
            pytaVSL.create_group('tv' + str(index), ['plane_horn_' + str(index), 'p_pub' + str(index)])

        ######## ORL - MEXPLIQUE-MOI
        ##### utiliser la même chose que clones pour groups
        ##### shaker les slides à l'intérieur d'un groupe, et mover les groups pour déplacer tout le monde.

    @pedalboard_button(2)
    def intro(self):
        """
        INTRO
        """
        self.start_scene('intro', lambda: [
            pytaVSL.position_overlay('Intro'),
            self.wait(0.1, 's'),
            self.shaking_tvs(),
            self.ronde_des_pubs()
        ])

    def shaking_tvs(self):
        for index in range(1,6):
            range_x = _rand()*0.01
            range_y = _rand()*0.01
            duration = _rand()*10
            pytaVSL.shaking_slide('plane_horn_' + str(index), 'position_x', range_x, duration)
            pytaVSL.shaking_slide('p_pub' + str(index), 'position_x', range_x, duration)
            pytaVSL.shaking_slide('plane_horn_' + str(index), 'position_y', range_y, duration, 'random')
            pytaVSL.shaking_slide('p_pub' + str(index), 'position_y', range_y, duration, 'random')


    def ronde_des_pubs(self):
        """
        RONDE DES PUBS
        """
        def desplats(plat):
            coords = {
                'main': [0, -0.07, -7.4],
                '1' : [-0.35, 0.2, -7.0],
                '2' : [-0.05, 0.2, -7.1],
                '3' : [0.25, 0.2, -7.2],
                '4' : [0.55, 0.2, -7.3],
                'scale_main': [0.8, 0.8],
                'scale_others': [0.3, 0.3],
            }

            pytaVSL.animate('tv' + str(plat), 'position', None, coords['main'], 1, 's', 'linear')
            pytaVSL.animate('tv' + str(plat), 'scale', None, coords['scale_main'], 1, 's', 'linear')

            for i in range(1,5):
                ind = i + plat
                if ind > 5:
                    ind = ind - 5
                pytaVSL.animate('tv' + str(ind), 'position', None, coords[str(i)], 1, 's', 'linear')
                pytaVSL.animate('tv' + str(ind), 'scale', None, coords['scale_others'], 1, 's', 'linear')

            pytaVSL.set('p_pub' + str(plat), 'video_time', 0, force_send=True),

        # def falldown(slide_name, chute, d):
        #     cur_y_pos = pytaVSL.get(slide_name, 'position_y')
        #
        #     self.start_scene('sequence/falldown_' + slide_name, lambda:[
        #         pytaVSL.animate(slide_name, 'position_y', None, cur_y_pos - chute, 0.3, 's', 'elastic'),
        #         self.wait(0.3, 's'),
        #         pytaVSL.animate(slide_name, 'position_y', None, cur_y_pos - chute + 0.001, 0.5, 's', 'random'),
        #         self.wait(0.5, 's'),
        #         pytaVSL.animate(slide_name, 'position_y', None, cur_y_pos, d-0.8, 's', 'linear'),
        #         self.wait(d-0.8, 's'),
        #         ]
        #     )
        #     return -1

        # def vibrate_pos(p, d):
        #         chute = -1
        #         factor = pytaVSL.get('p_pub' + str(p), 'scale')[0] * 0.01
        #         xdest = (_rand()+0.5)*factor-1.5*factor/2
        #         while xdest < factor/4 and xdest > -factor/4:
        #             xdest = xdest * 2
        #         ydest = _rand()*0.001+0.0003
        #
        #         if ydest < 0.0004 and d > 1.2 and chute == -1:
        #             chute = 0
        #             # if p == 1:
        #             #     chute = falldown('plane_horn', 2*10000*ydest*factor, d)
        #             #     falldown('p_pub1', 2*10000*ydest*factor, d)
        #             # else:
        #             chute = falldown('plane_horn_' + str(p), 2*10000*ydest*factor, d)
        #             falldown('p_pub' + str(p), 2*10000*ydest*factor, d)
        #             return
        #
        #
        #         # if p == 1:
        #         #     pytaVSL.animate('plane_horn', 'position_x', None, pytaVSL.get('plane_horn', 'position_x') + xdest, d, 's', 'linear-mirror', loop=True)
        #         #     pytaVSL.animate('plane_horn', 'position_y', None, pytaVSL.get('plane_horn', 'position_y') + ydest, d, 's', 'random-mirror', True)
        #         #     pytaVSL.animate('p_pub1', 'position_x', None, pytaVSL.get('p_pub1', 'position_x') + xdest, d, 's', 'linear-mirror', True)
        #         #     # pytaVSL.animate('plane_horn', 'position_y', None, pytaVSL.get('plane_horn', 'position_y') + ydest, d, 's', 'random')
        #         # else:
        #         pytaVSL.animate('plane_horn_' + str(p), 'position_x', None, pytaVSL.get('plane_horn_' + str(p), 'position_x') + xdest, d, 's', 'linear-mirror', True)
        #         pytaVSL.animate('plane_horn_' + str(p), 'position_y', None, pytaVSL.get('plane_horn_' + str(p), 'position_y') + ydest, d, 's', 'random-mirror', True)
        #         pytaVSL.animate('p_pub' + str(p), 'position_x', None, pytaVSL.get('p_pub' + str(p), 'position_x') + xdest, d, 's', 'linear-mirror', True)

        def desplats_chute(plat, duree_plat):
            for index in range(1,6):
                if not index == plat:
                    alea = _rand()
                    if alea < 0.85:
                        wait_coef = _rand()*0.2
                        fall_coef = _rand()*(1 - wait_coef - 0.5)
                        self.start_scene('sequence/wait_and_falldown_tv' + str(index), lambda: [
                            self.wait(wait_coef * duree_plat, 's'),
                            pytaVSL.falldown('tv' + str(index), alea * 0.25, duree_plat * fall_coef)
                        ])
                        return -1


        def desplats_scene(plat):
            if plat == 0:
                plat = 5
            duree_plat = pytaVSL.get('p_pub' + str(plat), 'video_end')
            self.start_scene('sequence/plat' + str(plat), lambda:[
                self.logger.info('Début scène des plats'),
                pytaVSL.animate('p_pub*', 'noise', 0, 1, 1, 's', 'random'),
                desplats(plat),
                pytaVSL.animate('p_pub*', 'noise', 1, 0, 1, 's', 'random'),
                self.wait(1.1, 's'),
                # vibrate_pos(1, 2.5),
                # vibrate_pos(2, 2),
                # vibrate_pos(3, 1.3),
                # vibrate_pos(4, 3),
                # vibrate_pos(5, 3.4),

                # self.start_sequence('plane_vibrate_pos', [{
                #     0.5: lambda: vibrate_pos(5, 3),
                #     1: lambda: vibrate_pos(1, 1.5),
                #     1.3: lambda: vibrate_pos(3, 1.3),
                #     2: lambda: vibrate_pos(2, 1),
                #     2.5: lambda: vibrate_pos(1, 2),
                #     2.6: lambda: vibrate_pos(3, 1.3),
                #     3: lambda: [vibrate_pos(2, 1), vibrate_pos(4, 4)],
                #     3.5: lambda: vibrate_pos(5, 2),
                #     3.9: vibrate_pos(3, 2.4),
                #     4: lambda: vibrate_pos(2, 2),
                #     4.5: lambda: vibrate_pos(1, 0.5)
                # }], loop=True),
                desplats_chute(plat, duree_plat - 1.1),
                self.wait(duree_plat - 1.1, 's'),
                self.logger.info('Fin scène des plats'),
                desplats_scene(plat-1)
            ])
        desplats_scene(4)

    @pedalboard_button(4)
    def chapitre1(self):
        """
        Switch vers chapitre 1
        """
        engine.set_route('Chapitre 1')

    @pedalboard_button(97)
    def preserve(self):
        self.start_scene('gnagna', lambda: [
            pytaVSL.animate('back', 'position_x', 0, 0.5, 5, 's', 'linear-mirror', loop=True),
            self.wait(2, 's'),
            pytaVSL.animate('back', 'position_y', 0, 0.5, 5, 's', 'random-mirror', loop=True)
        ])

    @pedalboard_button(98)
    def test(self):
        pytaVSL.create_group('lights', ['lights_stageleft', 'lights_stageright'])

    @pedalboard_button(99)
    def test2(self):
        pytaVSL.trijc_io('out', 'tuba', 1, 'elastic')

    @pedalboard_button(90)
    def testo(self):
        self.stop_scene('*')

    @pedalboard_button(89)
    def lopp_animation(self):
        pytaVSL.animate('back', 'position_x', 0, 0.5, 1, 's', 'elastic-mirror-inout', True)
