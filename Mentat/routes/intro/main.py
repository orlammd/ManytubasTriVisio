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
        pytaVSL.send('/pyta/unload', '*')
        pytaVSL.load_slides_from_dir('Common')
        pytaVSL.load_slides_from_dir('Chapitre1')
        pytaVSL.load_slides_from_dir('Chapitre2')
        pytaVSL.load_slides_from_dir('Chapitre3')
        pytaVSL.load_slides_from_dir('Chapitre4')
        pytaVSL.load_slides_from_dir('Chapitre5')
        pytaVSL.sync()

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

        for index in range (2,6):
            pytaVSL.create_clone('f_arabesque_1', 'f_arabesque_' + str(index))

        pytaVSL.create_clone('plane_horn_1', 'plane_horn_jc')
        for index in range(2,6):
            pytaVSL.create_clone('plane_horn_1', 'plane_horn_' + str(index))

        ### Create groups

        pytaVSL.create_group('t_trijc_lustre', ['sub_t_trijc_lustre_*'])

        for slides_group in [
            'trijc',
            't_trijc',
            'ot_trijc',
            'lights',
            ]:
            pytaVSL.create_group(slides_group, [slides_group + '*'])
        for slides_group in [
            'jack',
            'caesar',
            'manytubas',
            'tri',
            'visio',
            ]:
            pytaVSL.create_group('w_signs_' + slides_group, ['signs*' + slides_group])

        for index in range(1,6):
            pytaVSL.create_group('tv' + str(index), ['plane_horn_' + str(index), 'p_pub' + str(index)])

        pytaVSL.sync()

        # Create text slides
        # pytaVSL.send('/pyta/create_text', 'titre', 'sans')
        # pytaVSL.send('/pyta/create_text', 'soustitre', 'mono')

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
            range_x = (_rand() / 2 + 0.5) * 0.01
            range_y = _rand() * 0.01
            duration = (_rand() / 2 + 0.5) * 10
            pytaVSL.shaking_slide('plane_horn_' + str(index), 'position_x', range_x, duration)
            pytaVSL.shaking_slide('p_pub' + str(index), 'position_x', range_x, duration)
            pytaVSL.shaking_slide('plane_horn_' + str(index), 'position_y', range_y, duration, 'random')
            pytaVSL.shaking_slide('p_pub' + str(index), 'position_y', range_y, duration, 'random')


    def desplats(self, plat):
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

    def ronde_des_pubs(self):
        """
        RONDE DES PUBS
        """

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
                pytaVSL.animate('p_pub*', 'noise', 0, 1, 1, 's', 'random'),
                self.desplats(plat),
                pytaVSL.animate('p_pub*', 'noise', 1, 0, 1, 's', 'random'),
                self.wait(1.1, 's'),
                desplats_chute(plat, duree_plat - 1.1),
                self.wait(duree_plat - 1.1, 's'),
                desplats_scene(plat-1)
            ])

        desplats_scene(4)



    @pedalboard_button(3)
    def aspiration_des_pubs(self):
        """
        Aspiration des pubs
        """
        #### On stoppe la séquence de ronde, pour éviter que les valeurs ne changent au milieu de l'aspiration
        self.stop_scene('*')
        # self.stop_scene('sequence/wait_and_falldown_tv')
        start = 1
        zoom = 0
        for i in range(1,6):
            if(pytaVSL.get('tv' + str(i), 'scale')[0] > zoom):
                zoom = pytaVSL.get('tv' + str(i), 'scale')[0]
                start = i
        sorted = []
        for i in range(0,5):
            sorted.append(start + i if start + i < 6 else start + i - 5)
            # ranger dans l'ordre

        duration = 1

        plane_warp_1 = [0, -0.35]
        plane_warp_4 = [0, 0.63]

        pub_warp_1 = [-0.0755, -0.11]
        pub_warp_4 = [-0.0755, 0.86]

        def aspi_pub(index):
            pytaVSL.aspi_slide('plane_horn_' + str(index), plane_warp_1, plane_warp_4, duration,)
            pytaVSL.aspi_slide('p_pub' + str(index), pub_warp_1, pub_warp_4, duration)

        self.start_scene('sequence/aspi_pubs', lambda: [
            ### Aspiration des pubs
            pytaVSL.set('t_trijc_aspi', 'rotate_z', -5),
            pytaVSL.trijc_io('in', 'aspi', 2, 'linear'),
            self.wait(2, 's'),
            pytaVSL.animate('t_trijc_aspi', 'rotate_z', None, 0, 0.2, 's', 'elastic-inout'),
            # self.wait(0.2, 's'),
            aspi_pub(sorted[0]),
            self.wait(1.1, 's'),
            pytaVSL.animate('t_trijc_aspi', 'rotate_z', None, -5, 0.5, 's'),
            self.desplats(sorted[4]),
            self.wait(1.1, 's'),
            pytaVSL.animate('t_trijc_aspi', 'rotate_z', None, 0, 0.2, 's', 'elastic-inout'),
            # self.wait(0.2, 's'),
            aspi_pub(sorted[4]),
            self.wait(1.1, 's'),
            pytaVSL.animate('t_trijc_aspi', 'rotate_z', None, -5, 0.5, 's'),
            self.desplats(sorted[3]),
            self.wait(1.1, 's'),
            pytaVSL.animate('t_trijc_aspi', 'rotate_z', None, 0, 0.2, 's', 'elastic-inout'),
            # self.wait(0.2, 's'),
            aspi_pub(sorted[3]),
            self.wait(1.1, 's'),
            pytaVSL.animate('t_trijc_aspi', 'rotate_z', None, -5, 0.5, 's'),
            self.desplats(sorted[2]),
            self.wait(1.1, 's'),
            pytaVSL.animate('t_trijc_aspi', 'rotate_z', None, 0, 0.2, 's', 'elastic'),
            # self.wait(0.2, 's'),
            aspi_pub(sorted[2]),
            self.wait(1.1, 's'),
            pytaVSL.animate('t_trijc_aspi', 'rotate_z', None, -5, 0.5, 's'),
            self.desplats(sorted[1]),
            self.wait(1.1, 's'),
            pytaVSL.animate('t_trijc_aspi', 'rotate_z', None, 0, 0.2, 's', 'elastic'),
            # self.wait(0.2, 's'),
            aspi_pub(sorted[1]),
            self.wait(1.1, 's'),
            pytaVSL.trijc_io('out', 'aspi', 1, 'elastic'),
            self.wait(1.1, 's'),
            engine.set_route('Chapitre 1')
            ]
        )
