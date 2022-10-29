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

        # Chargement des vidéos
        self.start_scene('load_and_overlay', lambda: [
            self.aspi_pubs(),
            # pytaVSL.load_slides_from_dir('Chapitre1'),
            self.wait(0.5, 's'),
            # pytaVSL.position_overlay('Chapitre1')
        ])

    def aspi_pub(self, number):
        """
        Aspiration d'une pub
        """
        tv = 'plane_horn_' + str(number)
        p = 'p_pub' + str(number)

        pytaVSL.stop_animate(tv, 'position_x')
        pytaVSL.stop_animate(tv, 'position_y')

        pytaVSL.stop_animate(p, 'position_x')
        pytaVSL.stop_animate(p, 'position_y')


        self.start_scene('sequence/aspi_pub', lambda: [
            [
                pytaVSL.animate(tv, 'warp_1', [0, 0], [0, -0.35], 1, 's', 'elastic-inout'), pytaVSL.animate(tv, 'warp_4', [0, 0], [0, 0.63], 1, 's', 'elastic-inout'),
                pytaVSL.animate(p, 'warp_1', [0, 0], [-0.0755, -0.11], 1, 's', 'elastic-inout'), pytaVSL.animate(p, 'warp_4', [0, 0], [-0.0755, 0.86], 1, 's', 'elastic-inout')
                ],
            self.wait(0.8, 's'),
            pytaVSL.animate(tv, 'scale', None, [0.035, 0.035], 0.5, 's', 'elastic-inout' ), pytaVSL.animate(tv, 'position', None, [-0.33, 0.035, pytaVSL.get(tv, 'position_z')], 0.5, 's', 'elastic-inout'),
            pytaVSL.animate(p, 'scale', None, [0.035, 0.035], 0.5, 's', 'elastic-inout'), pytaVSL.animate(p, 'position', None, [-0.33, 0.035, pytaVSL.get(p, 'position_z')], 0.5, 's', 'elastic-inout'),
            self.wait(0.5, 's'),
            pytaVSL.set(tv, 'visible', 0),
            pytaVSL.set(p, 'visible', 0)
        ])


    def desaspis(self, plat):
        xyzpos = {
            'main': [0, -0.07, -7.5],
            '1' : [-0.35, 0.2, -7.1],
            '2' : [-0.05, 0.2, -7.2],
            '3' : [0.25, 0.2, -7.3],
            '4' : [0.55, 0.2, -7.4],
            'scale_main': [0.8, 0.8],
            'scale_others': [0.3, 0.3],
            'pmain': [0, -0.135, -7.49],
            'p1' : [-0.35, 0.175, -7.09],
            'p2' : [-0.05, 0.175, -7.19],
            'p3' : [0.25, 0.175, -7.29],
            'p4' : [0.55, 0.175, -7.39],
            'pscale_main': [0.465, 0.465],
            'pscale_others': [0.18, 0.18],
        }


        # if plat == 1:
        #     pytaVSL.animate('plane_horn', 'position', None, xyzpos['main'], 1, 's', 'linear')
        #     pytaVSL.animate('plane_horn', 'scale', None, xyzpos['scale_main'], 1, 's', 'linear')
        #
        # else:
        pytaVSL.animate('plane_horn_' + str(plat), 'position', None, xyzpos['main'], 1, 's', 'linear')
        pytaVSL.animate('plane_horn_' + str(plat), 'scale', None, xyzpos['scale_main'], 1, 's', 'linear')


        pytaVSL.animate('p_pub' + str(plat), 'position', None, xyzpos['pmain'], 1, 's', 'linear')
        pytaVSL.animate('p_pub' + str(plat), 'scale', None, xyzpos['pscale_main'], 1, 's', 'linear')

        for i in range(1,5):
            ind = i + plat
            if ind > 5:
                ind = ind - 5
            # if ind == 1:
            #     pytaVSL.animate('plane_horn', 'position', None, xyzpos[str(i)], 1, 's', 'linear')
            #     pytaVSL.animate('plane_horn', 'scale', None, xyzpos['scale_others'], 1, 's', 'linear')
            # else:
            pytaVSL.animate('plane_horn_' + str(ind), 'position', None, xyzpos[str(i)], 1, 's', 'linear')
            pytaVSL.animate('plane_horn_' + str(ind), 'scale', None, xyzpos['scale_others'], 1, 's', 'linear')
            pytaVSL.animate('p_pub' + str(ind), 'position', None, xyzpos['p' + str(i)], 1, 's', 'linear')
            pytaVSL.animate('p_pub' + str(ind), 'scale', None, xyzpos['pscale_others'], 1, 's', 'linear')


    def aspi_pubs(self):
        """
        Aspiration des pubs
        """
        #### On stoppe la séquence de ronde, pour éviter que les valeurs ne changent au milieu de l'aspiration
        self.stop_scene('sequence/plat')
        start = 1
        zoom = 0
        for i in range(1,6):
            if(pytaVSL.get('p_pub' + str(i), 'scale')[0] > zoom):
                zoom = pytaVSL.get('p_pub' + str(i), 'scale')[0]
                start = i
        sorted = []
        for i in range(0,5):
            sorted.append(start + i if start + i < 6 else start + i - 5)
            # ranger dans l'ordre

        self.start_scene('sequence/aspi_pubs', lambda: [
            ### Aspiration des pubs
            pytaVSL.trijc_io('in', 'aspi', 2, 'linear'),
            self.wait(2, 's'),
            self.aspi_pub(sorted[0]),
            self.wait(1.3, 's'),
            self.desaspis(sorted[4]),
            self.wait(1.1, 's'),
            self.aspi_pub(sorted[4]),
            self.wait(1.3, 's'),
            self.desaspis(sorted[3]),
            self.wait(1.1, 's'),
            self.aspi_pub(sorted[3]),
            self.wait(1.3, 's'),
            self.desaspis(sorted[2]),
            self.wait(1.1, 's'),
            self.aspi_pub(sorted[2]),
            self.wait(1.3, 's'),
            self.desaspis(sorted[1]),
            self.wait(1.1, 's'),
            self.aspi_pub(sorted[1]),
            # ASPIRATION
            self.wait(1, 's'),
            pytaVSL.trijc_io('out', 'aspi', 1, 'elastic'),
            ]
        )

    def lancementmiraye1(self):
        """
        Lancement Miraye Part 1
        """
        self.start_scene('sequence/lancementmirage1', lambda: [
            ### Lancement du mFilm
            pytaVSL.trijc_io('in', 'tuba', 1, 'elastic'),
            self.wait(1.2, 's'),
            pytaVSL.miraye_in('m_ch1-2', 1)
            ]
        )

    def bouclemiraye1(self):
        """
        Boucle Miraye pendant que JC...
        """
        self.start_scene('sequence/mirayeccanwait', lambda: [
            pytaVSL.sset_prop('m_ch1-2_waiting', 'position', [0.0915, 0.016, -9.91]),
            pytaVSL.sset_prop('m_ch1-2_waiting', 'zoom', [0.71]),
            pytaVSL.sset_prop('m_ch1-2_waiting', 'video_speed', [1]), pytaVSL.sset_prop('m_ch1-2_waiting', 'video_loop', [1]),
            [pytaVSL.sanimate_prop('m_ch1-2', 'noise', [0, 0.2, 0.2]), pytaVSL.sanimate_prop('m_ch1-2', 'rgbwave', [0, 0.5, 0.2])],
            self.wait(0.2, 's'),
            [pytaVSL.sset_prop('m_ch1-2_waiting', 'visible', [1]), pytaVSL.sset_prop('m_ch1-2', 'visible', [0])],
            [pytaVSL.sanimate_prop('m_ch1-2_waiting', 'noise', [0.2, 0, 0.5]), pytaVSL.sanimate_prop('m_ch1-2_waiting', 'rgbwave', [0.5, 0, 0.5])],
        ])

    def debouclemiraye1(self):
        """
        Boucle Miraye pendant que JC...
        """
        self.start_scene('sequence/mirayeccanwait', lambda: [
            pytaVSL.sset_prop('m_ch1-7', 'position', [0.0915, 0.016, -9.91]),
            pytaVSL.sset_prop('m_ch1-7_waiting', 'video_speed', [1]), pytaVSL.sset_prop('m_ch1-7', 'video_speed', [1]),
            [pytaVSL.sanimate_prop('m_ch1-2_waiting', 'noise', [0, 0.2, 0.2]), pytaVSL.sanimate_prop('m_ch1-2_waiting', 'rgbwave', [0, 0.5, 0.2])],
            self.wait(0.2, 's'),
            [pytaVSL.sset_prop('m_ch1-7', 'visible', [1]), pytaVSL.sset_prop('m_ch1-2_waiting', 'visible', [0])],
            [pytaVSL.sanimate_prop('m_ch1-7', 'noise', [0.2, 0, 0.5]), pytaVSL.sanimate_prop('m_ch1-7', 'rgbwave', [0.5, 0, 0.5])],
        ])


    def miraye1descend(self):
        """
        Miraye descend observer pendant que JC ...
        """
        #### ORL -> revoir quand set sera utilisé TODO
        pytaVSL.sanimate_prop('mirayelayout', 'zoom', [0.837, 0.837*0.3125, 1])
        pytaVSL.sanimate_prop('m_ch1-2_waiting', 'zoom', [0.71, 0.71*0.3125, 1])
        for s in ['m_ch1-2_waiting', 'mirayelayout']:
             pytaVSL.sanimate_prop(s, 'position_y', [0.016, -0.35 ,1] )

    def miraye1remonte(self):
        """
        Miraye descend observer pendant que JC ...
        """
        #### ORL -> revoir quand set sera utilisé TODO
        pytaVSL.sanimate_prop('mirayelayout', 'zoom', [0.837*0.3125, 0.837, 1])
        pytaVSL.sanimate_prop('m_ch1-2_waiting', 'zoom', [0.71*0.3125, 0.71, 1])
        for s in ['m_ch1-2_waiting', 'mirayelayout']:
             pytaVSL.sanimate_prop(s, 'position_y', [-0.35, 0.016, 1] )

    def actesJC(self):
        """
        Les actes de JC
        """
        pytaVSL.sset_prop('m_ch1-7', 'zoom', [0.71]),
        ### TODO mettre le placement ailleurs
        for i in range (3, 7):
            pytaVSL.sset_prop('p_ch1-' + str(i), 'position', [1, 0, -11])
            pytaVSL.sset_prop('p_ch1-' + str(i), 'zoom', [0.55])
            pytaVSL.sset_prop('p_ch1-' + str(i), 'visible', [1])
            pytaVSL.sset_prop('p_ch1-' + str(i), 'video_loop', [1])
            pytaVSL.sset_prop('p_ch1-' + str(i), 'video_time', [0])
            pytaVSL.sset_prop('p_ch1-' + str(i), 'video_speed', [1])


        self.start_scene('sequence/actesJC', lambda:[
            pytaVSL.sanimate_prop('p_ch1-3', 'position_x', [1, 0.09, 2]),
            self.wait(3, 's'),
            pytaVSL.sanimate_prop('p_ch1-3', 'position_x', [0.09, -1, 2]),
            pytaVSL.sset_prop('p_ch1-4', 'video_time', [0]),
            pytaVSL.sanimate_prop('p_ch1-4', 'position_x', [0.6, 0.09, 2]),
            self.wait(3, 's'),
            pytaVSL.sanimate_prop('p_ch1-4', 'position_x', [0.09, -1, 2]),
            pytaVSL.sset_prop('p_ch1-5', 'video_time', [0]),
            pytaVSL.sanimate_prop('p_ch1-5', 'position_x', [1, 0.09, 2]),
            self.wait(3, 's'),
            pytaVSL.sanimate_prop('p_ch1-5', 'position_x', [0.09, -1, 2]),
            pytaVSL.sset_prop('p_ch1-6', 'video_time', [0]),
            pytaVSL.sanimate_prop('p_ch1-6', 'position_x', [1, 0.09, 2]),
            self.wait(3, 's'),
            pytaVSL.sanimate_prop('p_ch1-6', 'position_x', [0.09, -1, 2]),
            self.wait(3, 's'),
            pytaVSL.sset_prop('p_ch1*', 'visible', [0]),
        ])

    @pedalboard_button(1)
    def intro(self):
        """
        Intro
        """
        self.start_scene('sequence/intro', lambda: [
            self.aspi_pubs(),
            self.wait(5, 's'),
            self.wait(1.2, 's'),
            self.lancementmiraye1(),
            self.wait(1.1, 's'),
            self.wait(pytaVSL.get('m_ch1-2', 'video_end'), 's'),
            self.bouclemiraye1(),
            self.wait(0.2, 's'),
            self.miraye1descend(),
            self.actesJC(),
            self.wait(13, 's'),

            self.miraye1remonte(),
            self.wait(1, 's'),
            self.debouclemiraye1(),
            ]
        )


    @pedalboard_button(90)
    def testo(self):
        """
        Intro
        """
        self.start_scene('sequence/intro', lambda: [
            self.bouclemiraye1(),
            self.wait(0.2, 's'),
            self.miraye1descend(),
            self.actesJC(),
            self.wait(13, 's'),

            self.miraye1remonte(),
            self.wait(1, 's'),
            self.debouclemiraye1(),
            ]
        )


    @pedalboard_button(2)
    def test(self):
        """
        INTRO
        """
        self.start_scene('sequence/aspimiraye', lambda: [
            [
                pytaVSL.sanimate_prop('m_ch1-2', 'warp_1', [0, 0, 0, -0.49, 1, 'elastic']), pytaVSL.sanimate_prop('m_ch1-2', 'warp_4', [0, 0, 0, 0.49, 1, 'elastic']),
                pytaVSL.sanimate_prop('mirayelayout', 'warp_1', [0, 0, 0, -0.49, 1, 'elastic']), pytaVSL.sanimate_prop('mirayelayout', 'warp_4', [0, 0, 0, 0.49, 1, 'elastic'])
                ],
            self.wait(0.8, 's'),
            pytaVSL.sanimate_prop('mirayelayout', 'zoom', [0.7, 0.035, 1, 'elastic' ]), pytaVSL.sanimate_prop('mirayelayout', 'position', [0, 0, 0, -0.3, -0.2, 0, 0.5, 'elastic']),
            pytaVSL.sanimate_prop('m_ch1-2', 'zoom', [0.7, 0.035, 1, 'elastic' ]), pytaVSL.sanimate_prop('m_ch1-2', 'position', [0, 0, 0, -0.3, -0.2, 0, 0.5, 'elastic']),
        ])

    @pedalboard_button(3)
    def outro(self):
        """
        OUTRO
        """
        pytaVSL.trijc_io('in')

    @pedalboard_button(4)
    def test2(self):
        """
        boucle_miraye
        """
        # pytavsl["m_ch1-2"].video_end

        self.start_scene('sequence/mirayeccanwait', lambda: [
            [pytaVSL.sanimate_prop('m_ch1-2', 'noise', [0, 0.2, 0.2]), pytaVSL.sanimate_prop('m_ch1-2', 'rgbwave', [0, 0.5, 0.2])],
            self.wait(0.2, 's'),
            [pytaVSL.sanimate_prop('m_ch1-2', 'noise', [0.2, 0, 0.5]), pytaVSL.sanimate_prop('m_ch1-2', 'rgbwave', [0.5, 0, 0.5])],
            self.start_sequence('bouclemiraye', [
                {
                    1: lambda: pytaVSL.sset_prop('m_ch1-2', 'video_time', [0]),
                    3: lambda: pytaVSL.sset_prop('m_ch1-2', 'video_time', [0])
                }
            ], loop=True)

        ])

    @pedalboard_button(5)
    def miraye_in(self):
        pytaVSL.miraye_in('m_ch1-1')

    @pedalboard_button(12)
    def stop(self):
        self.stop_sequence('*')

    @pedalboard_button(99)
    def testaspi(self):
        # self.aspi_pub()
        pytaVSL.animate('back', 'position_x', 0, 0.5, 1, 's', 'exponential-inout')
