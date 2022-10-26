from ..base import RouteBase, pedalboard_button
from .video import Video
from .light import Light
import time

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

            xyzpos = {
                'main': [0, -0.17, -17.5],
                '1' : [-0.35, 0.2, -17.1],
                '2' : [-0.05, 0.2, -17.2],
                '3' : [0.25, 0.2, -17.3],
                '4' : [0.55, 0.2, -17.4],
                'scale_main': [0.6, 0.6],
                'scale_others': [0.3, 0.3],
                'pmain': [0, -0.22, -17.49],
                'p1' : [-0.35, 0.18, -17.09],
                'p2' : [-0.05, 0.18, -17.19],
                'p3' : [0.25, 0.18, -17.29],
                'p4' : [0.55, 0.18, -17.39],
                'pscale_main': [0.35, 0.35],
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
                    pytaVSL.animate('plane_horn', 'position', None, xyzpos['1'], 1, 's', 'linear')
                    pytaVSL.animate('plane_horn', 'scale', None, xyzpos['scale_others'], 1, 's', 'linear')
                else:
                    pytaVSL.animate('plane_horn_' + str(ind), 'position', None, xyzpos['p' + str(i)], 1, 's', 'linear')
                    pytaVSL.animate('plane_horn_' + str(ind), 'scale', None, xyzpos['scale_others'], 1, 's', 'linear')
                pytaVSL.animate('p_pub' + str(ind), 'position', None, xyzpos['p' + str(i)], 1, 's', 'linear')
                pytaVSL.animate('p_pub' + str(ind), 'scale', None, xyzpos['pscale_others'], 1, 's', 'linear')

        self.logger.info(pytaVSL.get('p_pub1', 'video_end'))

        self.start_scene('sequence/plat1', lambda: [
            self.logger.info('starting scene'),
            desplats(1),
            self.wait(pytaVSL.get('p_pub1', 'video_end'), 's'),
            desplats(2),
            self.wait(pytaVSL.get('p_pub2', 'video_end'), 's'),
            desplats(3),
            self.wait(pytaVSL.get('p_pub3', 'video_end'), 's'),
            desplats(4),
            self.wait(pytaVSL.get('p_pub4', 'video_end'), 's'),
            desplats(5),
            self.wait(pytaVSL.get('p_pub5', 'video_end'), 's'),
        ])
        #
        # self.start_sequence('ronde_des_pubs', [
        #     {
        #     1: lambda: [
        #         self.logger.info('round 1'),
        #         pytaVSL.animate('plane_horn', 'position', None, xyzpos['main'], 1, 's', 'linear'),
        #         self.logger.info('round 1-2'),
        #         pytaVSL.animate('plane_horn_2', 'position', None, xyzpos['1'], 1, 's', 'linear'),
        #         pytaVSL.animate('plane_horn_3', 'position', None, xyzpos['2'], 1, 's', 'linear'),
        #         pytaVSL.animate('plane_horn_4', 'position', None, xyzpos['3'], 1, 's', 'linear'),
        #         pytaVSL.animate('plane_horn_5', 'position', None, xyzpos['4'], 1, 's', 'linear'),
        #         pytaVSL.animate('p_pub1', 'position', None, xyzpos['pmain'], 1, 's', 'linear'),
        #         pytaVSL.animate('p_pub2', 'position', None, xyzpos['p1'], 1, 's', 'linear'),
        #         pytaVSL.animate('p_pub3', 'position', None, xyzpos['p2'], 1, 's', 'linear'),
        #         pytaVSL.animate('p_pub4', 'position', None, xyzpos['p3'], 1, 's', 'linear'),
        #         pytaVSL.animate('p_pub5', 'position', None, xyzpos['p4'], 1, 's', 'linear'),
        #         self.logger.info('round 1-end')
        #     ],
        #
        #     3: lambda: [
        #         pytaVSL.animate('plane_horn_2', 'position', None, xyzpos['main'], 1, 's', 'linear'),
        #         pytaVSL.animate('plane_horn_3', 'position', None, xyzpos['1'], 1, 's', 'linear'),
        #         pytaVSL.animate('plane_horn_4', 'position', None, xyzpos['2'], 1, 's', 'linear'),
        #         pytaVSL.animate('plane_horn_5', 'position', None, xyzpos['3'], 1, 's', 'linear'),
        #         pytaVSL.animate('plane_horn', 'position', None, xyzpos['4'], 1, 's', 'linear'),
        #         pytaVSL.animate('p_pub2', 'position', None, xyzpos['pmain'], 1, 's', 'linear'),
        #         pytaVSL.animate('p_pub3', 'position', None, xyzpos['p1'], 1, 's', 'linear'),
        #         pytaVSL.animate('p_pub4', 'position', None, xyzpos['p2'], 1, 's', 'linear'),
        #         pytaVSL.animate('p_pub5', 'position', None, xyzpos['p3'], 1, 's', 'linear'),
        #         pytaVSL.animate('p_pub1', 'position', None, xyzpos['p4'], 1, 's', 'linear'),
        #         self.logger.info('youpe')
        #     ]
        #     },
        #     {
        #     1: lambda: [
        #         pytaVSL.animate('plane_horn_3', 'position', None, xyzpos['main'], 1, 's', 'linear'),
        #         pytaVSL.animate('plane_horn_4', 'position', None, xyzpos['1'], 1, 's', 'linear'),
        #         pytaVSL.animate('plane_horn_5', 'position', None, xyzpos['2'], 1, 's', 'linear'),
        #         pytaVSL.animate('plane_horn', 'position', None, xyzpos['3'], 1, 's', 'linear'),
        #         pytaVSL.animate('plane_horn_2', 'position', None, xyzpos['4'], 1, 's', 'linear'),
        #         pytaVSL.animate('p_pub3', 'position', None, xyzpos['pmain'], 1, 's', 'linear'),
        #         pytaVSL.animate('p_pub4', 'position', None, xyzpos['p1'], 1, 's', 'linear'),
        #         pytaVSL.animate('p_pub5', 'position', None, xyzpos['p2'], 1, 's', 'linear'),
        #         pytaVSL.animate('p_pub1', 'position', None, xyzpos['p3'], 1, 's', 'linear'),
        #         pytaVSL.animate('p_pub2', 'position', None, xyzpos['p4'], 1, 's', 'linear'),
        #         self.logger.info('youpu')
        #     ],
        #     3: lambda: [
        #         pytaVSL.animate('plane_horn_4', 'position', None, xyzpos['main'], 1, 's', 'linear'),
        #         pytaVSL.animate('plane_horn_5', 'position', None, xyzpos['1'], 1, 's', 'linear'),
        #         pytaVSL.animate('plane_horn', 'position', None, xyzpos['2'], 1, 's', 'linear'),
        #         pytaVSL.animate('plane_horn_2', 'position', None, xyzpos['3'], 1, 's', 'linear'),
        #         pytaVSL.animate('plane_horn_3', 'position', None, xyzpos['4'], 1, 's', 'linear'),
        #         pytaVSL.animate('p_pub4', 'position', None, xyzpos['pmain'], 1, 's', 'linear'),
        #         pytaVSL.animate('p_pub5', 'position', None, xyzpos['p1'], 1, 's', 'linear'),
        #         pytaVSL.animate('p_pub1', 'position', None, xyzpos['p2'], 1, 's', 'linear'),
        #         pytaVSL.animate('p_pub2', 'position', None, xyzpos['p3'], 1, 's', 'linear'),
        #         pytaVSL.animate('p_pub3', 'position', None, xyzpos['p4'], 1, 's', 'linear'),
        #         self.logger.info('youpa')
        #     ]
        #     },
        #     {
        #     1: lambda: [
        #         pytaVSL.animate('plane_horn_5', 'position', None, xyzpos['main'], 1, 's', 'linear'),
        #         pytaVSL.animate('plane_horn', 'position', None, xyzpos['1'], 1, 's', 'linear'),
        #         pytaVSL.animate('plane_horn_2', 'position', None, xyzpos['2'], 1, 's', 'linear'),
        #         pytaVSL.animate('plane_horn_3', 'position', None, xyzpos['3'], 1, 's', 'linear'),
        #         pytaVSL.animate('plane_horn_4', 'position', None, xyzpos['4'], 1, 's', 'linear'),
        #         pytaVSL.animate('p_pub5', 'position', None, xyzpos['pmain'], 1, 's', 'linear'),
        #         pytaVSL.animate('p_pub1', 'position', None, xyzpos['p1'], 1, 's', 'linear'),
        #         pytaVSL.animate('p_pub2', 'position', None, xyzpos['p2'], 1, 's', 'linear'),
        #         pytaVSL.animate('p_pub3', 'position', None, xyzpos['p3'], 1, 's', 'linear'),
        #         pytaVSL.animate('p_pub4', 'position', None, xyzpos['p4'], 1, 's', 'linear'),
        #         self.logger.info('youpi')
        #     ]
        #     }
        # ], loop = True)

    @pedalboard_button(98)
    def test(self):
        pytaVSL.trijc_io()

    @pedalboard_button(99)
    def test2(self):
        pytaVSL.trijc_io('out', 'tuba', 1, 'elastic')
