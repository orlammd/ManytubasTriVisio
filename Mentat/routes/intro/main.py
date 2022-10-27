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


        pytaVSL.load_slides_from_dir('Common')


    @pedalboard_button(2)
    def position_overlay(self):
        """
        POSITION OVERLAY
        """
        pytaVSL.position_overlay('Common')



    @pedalboard_button(3)
    def ronde(self):
        """
        RONDE DES PUBS
        """


        def desplats(plat):

            pytaVSL.set('p_pub*', 'video_loop', 1)
            pytaVSL.set('p_pub*', 'fish', 0.8)

            xyzpos = {
                'main': [0, -0.07, -17.5],
                '1' : [-0.35, 0.2, -17.1],
                '2' : [-0.05, 0.2, -17.2],
                '3' : [0.25, 0.2, -17.3],
                '4' : [0.55, 0.2, -17.4],
                'scale_main': [0.8, 0.8],
                'scale_others': [0.3, 0.3],
                'pmain': [0, -0.135, -17.49],
                'p1' : [-0.35, 0.175, -17.09],
                'p2' : [-0.05, 0.175, -17.19],
                'p3' : [0.25, 0.175, -17.29],
                'p4' : [0.55, 0.175, -17.39],
                'pscale_main': [0.465, 0.465],
                'pscale_others': [0.18, 0.18],
            }


            if plat == 1:
                pytaVSL.animate('plane_horn', 'position', None, xyzpos['main'], 1, 's', 'linear')
                pytaVSL.animate('plane_horn', 'scale', None, xyzpos['scale_main'], 1, 's', 'linear')

            else:
                pytaVSL.animate('plane_horn_' + str(plat), 'position', None, xyzpos['main'], 1, 's', 'linear')
                pytaVSL.animate('plane_horn_' + str(plat), 'scale', None, xyzpos['scale_main'], 1, 's', 'linear')


            pytaVSL.animate('p_pub' + str(plat), 'position', None, xyzpos['pmain'], 1, 's', 'linear')
            pytaVSL.animate('p_pub' + str(plat), 'scale', None, xyzpos['pscale_main'], 1, 's', 'linear')

            for i in range(1,5):
                ind = i + plat
                if ind > 5:
                    ind = ind - 5
                if ind == 1:
                    pytaVSL.animate('plane_horn', 'position', None, xyzpos[str(i)], 1, 's', 'linear')
                    pytaVSL.animate('plane_horn', 'scale', None, xyzpos['scale_others'], 1, 's', 'linear')
                else:
                    pytaVSL.animate('plane_horn_' + str(ind), 'position', None, xyzpos[str(i)], 1, 's', 'linear')
                    pytaVSL.animate('plane_horn_' + str(ind), 'scale', None, xyzpos['scale_others'], 1, 's', 'linear')
                pytaVSL.animate('p_pub' + str(ind), 'position', None, xyzpos['p' + str(i)], 1, 's', 'linear')
                pytaVSL.animate('p_pub' + str(ind), 'scale', None, xyzpos['pscale_others'], 1, 's', 'linear')

            pytaVSL.set('p_pub' + str(plat), 'video_time', 0, force_send=True),

        def falldown(slide_name, chute, d):
            cur_y_pos = pytaVSL.get(slide_name, 'position_y')

            self.logger.info('slide name: ' + slide_name)
            self.logger.info('y: ' + str(cur_y_pos))
            self.logger.info('chute: ' + str(chute))
            self.logger.info('durée: ' + str(d))

            self.start_scene('sequence/falldown_' + slide_name, lambda:[
                pytaVSL.animate(slide_name, 'position_y', None, cur_y_pos - chute, 0.3, 's', 'elastic'),
                self.wait(0.3, 's'),
                pytaVSL.animate(slide_name, 'position_y', None, cur_y_pos - chute + 0.001, 0.5, 's', 'random'),
                self.wait(0.5, 's'),
                pytaVSL.animate(slide_name, 'position_y', None, cur_y_pos, d-0.8, 's', 'linear'),
                self.wait(d-0.8, 's'),
                ]
            )
            return -1

        def vibrate_pos(p, d):
                chute = -1
                factor = pytaVSL.get('p_pub' + str(p), 'scale')[0] * 0.01
                xdest = (_rand()+0.5)*factor-1.5*factor/2
                while xdest < factor/4 and xdest > -factor/4:
                    xdest = xdest * 2
                ydest = _rand()*0.001+0.0003

                if ydest < 0.0004 and d > 1.2 and chute == -1:
                    chute = 0
                    if p == 1:
                        chute = falldown('plane_horn', 2*10000*ydest*factor, d)
                        falldown('p_pub1', 2*10000*ydest*factor, d)
                    else:
                        chute = falldown('plane_horn_' + str(p), 2*10000*ydest*factor, d)
                        falldown('p_pub' + str(p), 2*10000*ydest*factor, d)
                    return


                if p == 1:
                    pytaVSL.animate('plane_horn', 'position_x', None, pytaVSL.get('plane_horn', 'position_x') + xdest, d, 's', 'linear')
                    pytaVSL.animate('plane_horn', 'position_y', None, pytaVSL.get('plane_horn', 'position_y') + ydest, d, 's', 'random')
                    pytaVSL.animate('p_pub1', 'position_x', None, pytaVSL.get('p_pub1', 'position_x') + xdest, d, 's', 'linear')
                    # pytaVSL.animate('plane_horn', 'position_y', None, pytaVSL.get('plane_horn', 'position_y') + ydest, d, 's', 'random')
                else:
                    pytaVSL.animate('plane_horn_' + str(p), 'position_x', None, pytaVSL.get('plane_horn_' + str(p), 'position_x') + xdest, d, 's', 'linear')
                    pytaVSL.animate('plane_horn_' + str(p), 'position_y', None, pytaVSL.get('plane_horn_' + str(p), 'position_y') + ydest, d, 's', 'random')
                    pytaVSL.animate('p_pub' + str(p), 'position_x', None, pytaVSL.get('p_pub' + str(p), 'position_x') + xdest, d, 's', 'linear')

        def desplats_scene(plat):
            if plat == 6:
                plat = 1
            self.start_scene('sequence/plat' + str(plat), lambda:[
                self.logger.info('Début scène des plats'),
                pytaVSL.animate('p_pub*', 'noise', 0, 1, 1, 's', 'random'),
                desplats(plat),
                pytaVSL.animate('p_pub*', 'noise', 1, 0, 1, 's', 'random'),
                self.wait(1.1, 's'),
                vibrate_pos(2, 2),
                vibrate_pos(3, 1.3),
                vibrate_pos(4, 3),
                vibrate_pos(5, 0.5),
                self.start_sequence('plane_vibrate_pos', [{
                    0.5: lambda: vibrate_pos(5, 3),
                    1: lambda: vibrate_pos(1, 1.5),
                    1.3: lambda: vibrate_pos(3, 1.3),
                    2: lambda: vibrate_pos(2, 1),
                    2.5: lambda: vibrate_pos(1, 2),
                    2.6: lambda: vibrate_pos(3, 1.3),
                    3: lambda: [vibrate_pos(2, 1), vibrate_pos(4, 4)],
                    3.5: lambda: vibrate_pos(5, 2),
                    3.9: vibrate_pos(3, 2.4),
                    4: lambda: vibrate_pos(2, 2),
                    4.5: lambda: vibrate_pos(1, 0.5)
                }], loop=True),
                self.wait(5-1.1, 's'), #pytaVSL.get('p_pub' + str(plat), 'video_end'), 's'),
                self.logger.info('Fin scène des plats'),
                desplats_scene(plat+1)
            ])


        desplats_scene(1)


    @pedalboard_button(98)
    def test(self):
        pytaVSL.trijc_io()

    @pedalboard_button(99)
    def test2(self):
        pytaVSL.trijc_io('out', 'tuba', 1, 'elastic')

    @pedalboard_button(90)
    def testo(self):
        self.stop_scene('*')
