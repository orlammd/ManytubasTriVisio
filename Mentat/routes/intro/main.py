from ..base import RouteBase, pedalboard_button
from .video import Video
from .light import Light

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

        xyzpos = {
            'main': [0, -0.17, -17.5],
            '1' : [-0.35, 0.2, -17.1],
            '2' : [-0.05, 0.2, -17.2],
            '3' : [0.25, 0.2, -17.3],
            '4' : [0.55, 0.2, -17.4]
        }
        self.start_scene('load_and_overlay', lambda: [
            pytaVSL.load_slides_from_dir('Common'),
            self.wait(0.5, 's'),
            pytaVSL.position_overlay('Common'),
            self.wait(10, 's'),

            self.start_sequence('ronde_des_pubs', [
                {
                1: lambda: [
                    pytaVSL.animate('plane_horn', 'position', None, xyzpos['main'], 1, 's', 'linear'),
                    pytaVSL.animate('plane_horn_2', 'position', None, xyzpos['1'], 1, 's', 'linear'),
                    pytaVSL.animate('plane_horn_3', 'position', None, xyzpos['2'], 1, 's', 'linear'),
                    pytaVSL.animate('plane_horn_4', 'position', None, xyzpos['3'], 1, 's', 'linear'),
                    pytaVSL.animate('plane_horn_5', 'position', None, xyzpos['4'], 1, 's', 'linear'),
                ],

                3: lambda: [
                    pytaVSL.animate('plane_horn_2', 'position', None, xyzpos['main'], 1, 's', 'linear'),
                    pytaVSL.animate('plane_horn_3', 'position', None, xyzpos['1'], 1, 's', 'linear'),
                    pytaVSL.animate('plane_horn_4', 'position', None, xyzpos['2'], 1, 's', 'linear'),
                    pytaVSL.animate('plane_horn_5', 'position', None, xyzpos['3'], 1, 's', 'linear'),
                    pytaVSL.animate('plane_horn', 'position', None, xyzpos['4'], 1, 's', 'linear'),
                ]
                },
                {
                1: lambda: [
                    pytaVSL.animate('plane_horn_3', 'position', None, xyzpos['main'], 1, 's', 'linear'),
                    pytaVSL.animate('plane_horn_4', 'position', None, xyzpos['1'], 1, 's', 'linear'),
                    pytaVSL.animate('plane_horn_5', 'position', None, xyzpos['2'], 1, 's', 'linear'),
                    pytaVSL.animate('plane_horn', 'position', None, xyzpos['3'], 1, 's', 'linear'),
                    pytaVSL.animate('plane_horn_2', 'position', None, xyzpos['4'], 1, 's', 'linear'),
                ],
                3: lambda: [
                    pytaVSL.animate('plane_horn_4', 'position', None, xyzpos['main'], 1, 's', 'linear'),
                    pytaVSL.animate('plane_horn_5', 'position', None, xyzpos['1'], 1, 's', 'linear'),
                    pytaVSL.animate('plane_horn', 'position', None, xyzpos['2'], 1, 's', 'linear'),
                    pytaVSL.animate('plane_horn_2', 'position', None, xyzpos['3'], 1, 's', 'linear'),
                    pytaVSL.animate('plane_horn_3', 'position', None, xyzpos['4'], 1, 's', 'linear'),
                ]
                },
                {
                1: lambda: [
                    pytaVSL.animate('plane_horn_5', 'position', None, xyzpos['main'], 1, 's', 'linear'),
                    pytaVSL.animate('plane_horn', 'position', None, xyzpos['1'], 1, 's', 'linear'),
                    pytaVSL.animate('plane_horn_2', 'position', None, xyzpos['2'], 1, 's', 'linear'),
                    pytaVSL.animate('plane_horn_3', 'position', None, xyzpos['3'], 1, 's', 'linear'),
                    pytaVSL.animate('plane_horn_4', 'position', None, xyzpos['4'], 1, 's', 'linear'),
                ]
                }
            ], loop = True)
        ])

    @pedalboard_button(2)
    def test(self):
        """
        INTRO
        """
        pytaVSL.trijc_io()

    @pedalboard_button(3)
    def test2(self):
        """
        INTRO
        """
        pytaVSL.trijc_io('out', 'tuba', 1, 'elastic')

    @pedalboard_button(4)
    def test3(self):
        pytaVSL.set('plane_horn', 'scale', 0.7, 0.7)
        pytaVSL.animate('plane_horn', 'rotate_z', 0, 180, 1, 's', 'linear')

        # pytaVSL.animate('plane_horn', 'position', None, [0, -0.17, -17.5], 1, 's', 'linear'),
        # pytaVSL.animate('plane_horn_2', 'position', None, [-0.35, 0.2, -17.1], 1, 's', 'linear'),
        # pytaVSL.animate('plane_horn_3', 'position', None, [-0.05, 0.2, -17.2], 1, 's', 'linear'),
        # pytaVSL.animate('plane_horn_4', 'position', None, [0.25, 0.2, -17.3], 1, 's', 'linear'),
        # pytaVSL.animate('plane_horn_5', 'position', None, [0.55, 0.2, -17.4], 1, 's', 'linear'),
