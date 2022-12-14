from mentat import Module
from random import randint, random as _rand
from os import listdir as _ls
import toml
import time

class Slide(Module):
        """
        PytaVSL Slide
        """

        def __init__(self, *args, **kwargs):

            super().__init__(*args, **kwargs)

            self.ping = False
            self.ready = False
            self.query_done = False

        def query_slide_state(self):
            if self.query_done:
                return
            if not self.ping:
                # ping jusqu'à ce que le slide existe
                self.send('/pyta/slide/%s/ping' % self.name, self.engine.port)
            else:
                # ping ok ? on peut demander les parametres
                self.query_done = True
                self.send('/pyta/slide/%s/get' % self.name, '*', self.engine.port)


class PytaVSL(Module):
    """
    VJing Producer
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.path_to_pyta = '/home/jeaneudes/OrageOTournage/ManytubasTriVisio/PytaVSL'

        self.slides = []

        self.slide_params = ['visible', 'position', 'position_x', 'position_y', 'position_z', 'rotate', 'rotate_x', 'rotate_y', 'rotate_z', 'scale', 'zoom',
            'video_time', 'video_speed', 'video_loop', 'video_end', 'rgbwave', 'noise', 'warp_1', 'warp_2', 'warp_3', 'warp_4', 'fish', 'noise']

        self.send('/pyta/subscribe', 'status', 2001)
        self.send('/pyta/subscribe', 'status', 23456)

        # self.add_event_callback('parameter_changed', self.parameter_changed)


        # Objects JC Manytubas
        ### TODO -> à re-ranger de manière à factoriser trijc, t_trijc et ot_trijc
        self.m_TriJC = ['trijc_socle', 'trijc_tarte', 'trijc_head', 'trijc_souffle']
        self.t_TriJC = ['t_trijc_tuba', 't_trijc_aspi', 't_trijc_aimant', 't_trijc_compas']
        self.ot_TriJC = ['ot_trijc_taser']

        self.TriJC_xinpos = 0
        self.TriJC_xoutoffset = -0.3
        self.t_TriJC_xoffset = -0.415


        self.get_excluded_parameters = [
            'position_x',
            'position_y',
            'position_z',
            'rotate_x',
            'rotate_y',
            'rotate_z',
            'zoom'
        ]

        # reset pyta
        # remove all slides
        self.send('/pyta/slide/*/remove')

        # get text slides
        # self.send('/pyta/text/*/get', 'visible', self.engine.port)

        self.status = 'ready'

    def create_clone(self, src, dest):
        if dest not in self.submodules:
            self.status == 'loading'
            slide = Slide(dest, parent=self)
            self.add_submodule(slide)
            self.send('/pyta/clone', src, dest)
            self.logger.info('Clone ' + dest + ' created from ' + src)


    def create_group(self, group, slides):
        # if len(slides) > 1:
        s = '{'
        i = 0
        while i < len(slides):
            if i > 0:
                s = s + ','
            s = s + slides[i]
            i = i+1
        s = s + '}'
        self.status == 'loading'
        if group not in self.submodules:
            slide = Slide(group, parent=self)
            self.add_submodule(slide)
        else:
            self.submodules[group].reset()
        self.send('/pyta/group', s, group)
        self.logger.info('Group ' + group + ' created with: ' + s)


    def load_slide(self, f):
        """
        Chargement + Suivi d'un nouveau calque
        """

        dir = f.partition('/')[0]
        if dir == 'Common':
            slide_name = f.partition('/')[2].partition('/')[2].partition('.')[0]
        else:
            slide_name = f.partition('/')[2].partition('.')[0]

        slide_name = slide_name.lower()

        if slide_name not in self.submodules:
            self.status == 'loading'
            slide = Slide(slide_name, parent=self)
            self.add_submodule(slide)
            self.send('/pyta/load', f)

    def load_slides_from_dir(self, dir='Common'):
        """
        Chargement des calques
        """

        self.logger.info('load slides from dir: ' + dir)

        if dir == 'Common':
            for d in _ls(self.path_to_pyta + '/' + dir):
                if not d == 'overlay':
                    filelist = _ls(self.path_to_pyta + '/' + dir + '/' + d)
                    for f in filelist:
                        if not f == 'overlay':
                            self.load_slide(dir + "/" + d + "/" + f)
        else:
            filelist = _ls(self.path_to_pyta + '/' + dir)
            for f in filelist:
                if not f == 'overlay':
                    self.load_slide(dir + "/" + f)

    def save_state(self, chapter):
        self.save(chapter + '.overlay', omit_defaults = True)

    def position_overlay(self, overlay='Common'):
        """
        Position des éléments de décor
        """
        self.logger.info('Positionning overlay ' + overlay)

        self.load(overlay + '.overlay')


########################## TRIJC
    def check_jack_caesar_consistency(self):
        pos = 0
        firstpass = True
        for slide_name in self.m_TriJC:
            if self.get(slide_name, 'position_x') == pos or firstpass == True:
                pos = self.get(slide_name, 'position_x')
                firstpass = False
                return -1
            else:
                self.logger.info('TriJC est dans un état déplorable')
                return 0

    def trijc_io(self, direction='in', tool="tuba", duration=0.5, easing='linear'):

        if self.check_jack_caesar_consistency():
            if direction == 'in':
                end = self.TriJC_xinpos
            elif direction == 'out':
                end = self.TriJC_xoutoffset

            y = self.get('trijc_head', 'position_y')
            t_y = self.get('t_trijc_' + tool, 'position_y')
            t_end = end + self.t_TriJC_xoffset

            self.set('t_trijc_' + tool, 'rotate_z', 0)

            self.start_scene('sequences/triJC_io', lambda: [
                [self.set('trijc*', 'visible', 1), self.set('t_trijc_*', 'visible', 0), self.set('t_trijc_' + tool, 'visible', 1)],
                [self.animate('trijc_*', 'position_x', None, end, duration, 's', easing), self.animate('t_trijc_*', 'position_x', None, t_end, duration, 's', easing)],
                [self.animate('trijc_*', 'position_y', y, y + 0.01, duration/2., 's', 'random'), self.animate('t_trijc_' + tool, 'position_y', t_y, t_y + 0.01, duration/2., 's', 'random')],
                self.wait(duration/2., 's'),
                [self.animate('trijc_*', 'position_y', y + 0.01, y, duration/2., 's', 'random'), self.animate('t_trijc_' + tool, 'position_y', t_y + 0.01, t_y, duration/2., 's', 'random')]
                ]
            )
        else:
            self.logger.info('Aborting TriJC IO animation')

    def trijc_change_tool(self, end_tool):
        """
        Changing the tool used by TriJC
        """
        init_tool = ""
        for slide_name in self.submodules:
            if slide_name.startswith('t_trijc_'):
                if self.get(slide_name, 'visible'):
                    init_tool = slide_name

        self.logger.info(init_tool + ' -> ' + end_tool)

        self.start_scene('changing_tool', lambda: [
            self.animate(init_tool, 'rotate_z', None, 90, 0.1, 's'),
            self.wait(0.1, 's'),
            self.animate('t_trijc_' + end_tool, 'rotate_z', 90, 0, 0.2, 's', 'elastic-inout'),
            self.set(init_tool, 'visible', 0),
            self.set('t_trijc_' + end_tool, 'visible', 1),
        ])

    def trijc_turn_lights(self, on='on', duration=1):
        dest = 0 if on == 'off' else 1
        angle = 360 * duration if on == 'off' else -360 * duration
        self.animate('sub_t_trijc_lustre_allume', 'alpha', None, dest, duration)
        self.animate('sub_t_trijc_lustre_potard', 'rotate_z', None, angle, duration)


    def aspi_slide(self, slide_name, warp_1, warp_4, duration):
        """
        Aspire une slide ou plusieurs slides dans l'aspi de trijc
        """
        old_z = self.get(slide_name, 'position_z')

        oscil_d = 2/3 * duration
        away_d = 1/3 * duration
        self.start_scene('sequence/aspi_pub' + slide_name, lambda: [
            self.animate(slide_name, 'rgbwave', None, 0.9, duration, 's', 'exponential-inout'),
            self.animate(slide_name, 'warp_1', None, warp_1, oscil_d, 's', 'elastic-inout'),
            self.animate(slide_name, 'warp_4', None, warp_4, oscil_d, 's', 'elastic-inout'),
            self.wait(0.7 * oscil_d, 's'),
            self.animate(slide_name, 'scale', None, [0.035, 0.035], away_d * 0.9, 's', 'exponential-inout' ), self.animate(slide_name, 'position', None, [-0.33, 0.035, self.get(slide_name, 'position_z')], away_d * 0.95, 's', 'exponential-inout'),
            self.animate(slide_name, 'alpha', None, 0.1, away_d * 0.8, 's', 'exponential-out'),
            self.wait(away_d, 's'),
            self.set(slide_name, 'visible', 0),

            self.set(slide_name, 'visible', 0),
            self.submodules[slide_name].reset(),
            self.set(slide_name, 'position_z', old_z),

        ])

########################## TRIJC

########################## SIGNS
    def signs_io(self, direction='in', together=False, duration=1, easing='linear'):
        """
        Remontée et descente des panneaux
        """
        if direction == 'out':
            dest = 0.5
        if direction == 'in':
            dest = 0

        if together:
            self.animate('w_signs*', 'position_y', None, dest, duration, 's', easing)
        else:
            for slide_name in self.submodules:
                if ('w_signs_' in slide_name):
                    sigma = _rand()
                    if sigma > 0.5:
                        easing = 'elastic-inout'
                    self.animate(slide_name, 'position_y', None, dest, (1 + sigma)*duration, 's', easing)


########################## SIGNS

########################## MIRAYE

    def miraye_in(self, filename, duration=1, easing='linear'):
        """
        Having Miraye Leparket starting her storytelling
        """
        '''
            [orig, dest]: x, y, z, zoom, rotate_z
        '''
        orig = {
            "x": -0.38,
            "y": -0.025,
            "z": -10,
            "zo": 0.04,
            "rot": -140
        }
        dest = {
            "x": 0.092,
            "y": 0.016,
            "z": -10,
            "zo": 0.837,
            "rot": -720
        }


##### On peut s'en passer ?
        self.set('m_iraye', 'position', orig['x'], orig['y'], orig['z'])
        self.set('m_iraye', 'scale', orig['zo'], orig['zo'])
        self.set('m_iraye', 'rotate_z', orig['rot'])
##### On peut s'en passer ?


##### A virer
        self.set('m_ch*', 'visible', 0)
        self.set('m_*', 'warp_1', 0, 0)
        self.set('m_*', 'warp_4', 0, 0)
        self.set('m_ch*', 'scale', 0.848, 0.848)
        self.set('m_layout', 'scale', 1, 1)
##### A virer


        climax_y = 0.3
        etape_zoom = 0.4 * dest["zo"]
        move_duration= 3/4 * duration
        zoom_duration = (1 - move_duration) * duration
        self.start_scene('sequences/miraye_in', lambda:[
            self.set(filename, 'video_time', 0),
            self.set(filename, 'video_speed', 1, force_send=True),
            self.set(filename, 'visible', 1),
            self.set('m_layout', 'visible', 1),
            self.animate('t_trijc_tuba', 'rotate_z', None, -7, 0.4, 's', 'elastic-inout'),
            self.wait(0.2, 's'),
            self.set('m_iraye', 'visible', 1),
            self.animate('m_iraye', 'position_x', None, dest["x"], move_duration, 's', easing),
            self.animate('m_iraye', 'rotate_z', None, dest["rot"], move_duration, 's', easing),
            self.animate('m_iraye', 'scale', None, [etape_zoom, etape_zoom], move_duration, 's', easing),
            self.animate('m_iraye', 'position_y', None, climax_y, move_duration * 1/2, 's', easing),
            self.wait(1/2.*duration, 's'),
            self.animate('m_iraye', 'position_y', None, dest["y"], zoom_duration, 's', easing),
            self.wait(1/4.*duration, 's'),
            self.animate('m_iraye', 'scale', None, [dest["zo"], dest["zo"]], zoom_duration, 's', easing),
            self.animate('t_trijc_tuba', 'rotate_z', None, 0, 0.4, 's', 'random'),
        ])

    def m_noisy_switch_video(self, orig, dest, duration):
        """
        Switching from one video to another in m_layout with a noisy state in between
        """

        w_coef = _rand() * 0.8

        self.start_scene('sequence/' + orig + '_-_' + dest, lambda: [
            self.set(dest, 'rgbwave', w_coef),
            self.set(dest, 'noise', 1.0),
            self.animate(orig, 'noise', None, 1.0, duration / 2, 's'),
            self.animate(orig, 'rgbwave', None, w_coef, duration / 2, 's'),
            self.wait(0.25, 's'),
            self.set(dest, 'visible', 1),
            self.set(dest, 'video_time', 0, force_send=True),
            self.set(dest, 'video_speed', 1),
            self.set(orig, 'visible', 0),
            self.animate(dest, 'noise', 1.0, 0.0, duration / 2, 's'),
            self.animate(dest, 'rgbwave', None, 0.0, duration / 2, 's'),
            self.set(orig, 'noise', 0),
            self.set(orig, 'rgbwave', 0)
            ]
        )

    def m_switch_video(self, orig, dest):
        """
        Switching from one video to another in m_layout with a noisy state in between
        """

        w_coef = _rand() * 0.8

        self.start_scene('sequence/' + orig + '_-_' + dest, lambda: [
            self.set(dest, 'visible', 1),
            self.set(dest, 'video_time', 0, force_send=True),
            self.set(dest, 'video_speed', 1),
            self.set(orig, 'visible', 0),
            ]
        )


    def miraye_out(self, duration, easing):
        """
        Having Miraye Leparket stopping her storytelling
        """
        pass

    # def title_scene(self, title, duration):
    #     """
    #     Affiche le titre (scène)
    #     """
    #     segments = title.split(' ')
    #     segments_duration = {}
    #     total_length = len(title)
    #     atom = duration / total_length
    #
    #     # On sépare les mots et on compare leur nombre de lettres
    #     for segment in segments:
    #         segments_duration[segment] = atom * len(segment) / total_length
    #         self.set('titre', 'text', segment)
    #         self.wait(segments_duration[segment], 's')
    #         self.logger.info('titre segment:' + segment)
    #
    #
    #
    def display_title(self, title, duration):
        """
        Affiche le titre
        """
        self.logger.info('Display Title: ' + title + ' in ' + str(duration) + ' s...')
        # self.start_scene('display_title', self.title_scene(title, duration))


########################## Miraye

########################## FILM

    def movie_in(self, movie, duration, easing='linear', zoom=0.95, x=0, y=0, z=5, y_arabesque=3.04):
        """
        Having Moving coming to front
        """
        orig = {
            "x": -0.38,
            "y": -0.05,
            "z": 5,
            "zo": 0.3,
            "rot": -140
        }
        dest = {
            "x": x,
            "y": y,
            "z": z,
            "y_arabesque" : y_arabesque,
            "zo": zoom,
            "rot": -720
        }

        climax_y = 0.3
        etape_zoom = 0.4 * dest["zo"]
        # move_duration= 1/2.5 * duration
        complete_duration = 2.5 * duration
        zoom_duration = (1 - duration) * complete_duration
        self.start_scene('sequences/movie_in', lambda:[
            self.set(movie, 'video_time', 0, force_send=True),
            self.set(movie, 'video_speed', 1),
            self.set(movie, 'visible', 1),

            self.animate('t_trijc_tuba', 'rotate_z', None, -7, 0.4, 's', 'elastic-inout'),
            self.wait(0.2, 's'),
            self.set(movie, 'scale', 1.0, 0),
            self.set('f_ilm', 'visible', 1),


            self.animate('f_ilm', 'position_x', None, dest["x"], duration, 's', easing),
            self.animate('f_ilm', 'rotate_z', None, dest["rot"], duration, 's', easing),
            self.animate('f_ilm', 'scale', None, [dest["zo"], dest["zo"]], duration, 's', easing),
            self.animate('f_ilm', 'position_y', None, climax_y, duration * 1/2, 's', easing),
            self.wait(1/2.*duration, 's'),
            self.animate('f_ilm', 'position_y', None, dest["y"], duration * 1/2, 's', easing),
            self.wait(duration, 's'),

            self.trijc_change_tool('compas'),
            self.set(movie, 'video_time', 0),
            self.animate('t_trijc_compas', 'rotate_z', None, 45, zoom_duration, 's'),
            self.animate(movie, 'scale', None, [1.0, 1.0], zoom_duration, 's'),
            self.animate('f_arabesque_1', 'position_y', None, dest["y_arabesque"], zoom_duration, 's'),
            self.animate('f_arabesque_2', 'position_y', None, -dest["y_arabesque"], zoom_duration, 's'),
            self.signs_io('out', together=False, duration=complete_duration),
            self.wait(complete_duration / 2, 's'),
            self.animate('t_trijc_compas', 'rotate_z', None, 0, 0.1, 's', 'elastic-inout'),
            self.animate('lights*', 'alpha', None, 0.3, complete_duration, 's', 'linear'),
            self.trijc_io('out', 'compas', zoom_duration + 0.5)
        ])

    def f_noisy_switch_video(self, orig, dest, duration):
        """
        Switching from one video to another in f_ilm with a noisy state in between
        """

        w_coef = _rand() * 0.8

        self.start_scene('sequence/' + orig + '_-_' + dest, lambda: [
            self.set(dest, 'rgbwave', w_coef),
            self.set(dest, 'noise', 1.0),
            self.animate(orig, 'noise', None, 1.0, duration / 2, 's'),
            self.animate(orig, 'rgbwave', None, w_coef, duration / 2, 's'),
            self.wait(0.25, 's'),
            self.set(dest, 'visible', 1),
            self.set(dest, 'video_time', 0, force_send=True),
            self.set(dest, 'video_speed', 1),
            self.set(orig, 'visible', 0),
            self.animate(dest, 'noise', 1.0, 0.0, duration / 2, 's'),
            self.animate(dest, 'rgbwave', None, 0.0, duration / 2, 's'),
            self.set(orig, 'noise', 0),
            self.set(orig, 'rgbwave', 0)
            ]
        )


    def f_switch_video(self, orig, dest):
        """
        Switching from one video to another in f_ilm
        """

        self.start_scene('sequence/' + orig + '_-_' + dest, lambda: [
            self.set(dest, 'visible', 1),
            self.set(dest, 'video_time', 0, force_send=True),
            self.set(dest, 'video_speed', 1),
            self.set(orig, 'visible', 0),
            ]
        )


    def movie_out(self, duration, easing):
        """
        Having Movie going back
        """
        pass

    # def movie_split(self, left_slide, left_position=[-0.35, 0.15], left_scale=[0.3, 0.3], right_movie, right_position=[0.1, -0.1], right_scale=[0.6, 0.6], trijc_in_duration=0.2, scale_duration=1, move_duration=1, easing='linear'):
    #     """
    #     Having several movies being split over the screen
    #     """
    #
    #     self.create_group('f_ilm_2', ['f_arabesques_2', right_movie])
    #
    #     climax_y = 0.3
    #     etape_zoom = [0.4 * r_scale for r_scale in right_scale]
    #     # move_duration= 1/2.5 * duration
    #     complete_duration = 2.5 * duration
    #     zoom_duration = (1 - duration) * complete_duration
    #     self.set(right_movie, 'video_time', 0),
    #     self.set(right_movie, 'video_speed', 1),
    #     self.set(right_movie, 'visible', 1),
    #
    #     dest =
    #
    #     self.start_scene('sequence/movie_split', lambda: ([
    #         self.trijc_io('in', 'compas', trijc_in_duration, 'elastic-inout'),
    #         self.wait(trijc_in_duration, 's'),
    #         self.animate('t_trijc_compas', 'rotate_z', None, 10, scale_duration / 2, 's', 'elastic-inout'),
    #         self.animate(left_slide, 'scale', None, [l_scale * 2 for l_scale in left_scale], scale_duration / 2, 's', 'elastic-inout'),
    #         self.wait(scale_duration / 2, 's'),
    #         self.trijc_change_tool('aimant'),
    #         self.animate(left_slide, 'scale', None, left_scale, scale_duration / 2, 's', easing),
    #         self.wait(scale_duration / 2, 's'),
    #         self.animate('t_trijc_aimant', 'rotate_z', None, -45, move_duration, 's'),
    #         self.animate(left_slide, 'position_x', None, left_position[0], move_duration, 's', easing),
    #         self.animate(left_slide, 'position_y', None, left_position[1], move_duration, 's', easing),
    #         self.wait(0.5, 's'),
    #         self.trijc_change_tool('tuba'),
    #
    #
    #
    #         self.animate('t_trijc_tuba', 'rotate_z', None, -7, 0.4, 's', 'elastic-inout'),
    #         self.wait(0.2, 's'),
    #         self.set('f_ilm_2', 'visible', 1),
    #
    #         self.animate('f_ilm', 'position_x', None, dest["x"], duration, 's', easing),
    #         self.animate('f_ilm', 'rotate_z', None, dest["rot"], duration, 's', easing),
    #         self.animate('f_ilm', 'scale', None, [dest["zo"], dest["zo"]], duration, 's', easing),
    #         self.animate('f_ilm', 'position_y', None, climax_y, duration * 1/2, 's', easing),
    #         self.wait(1/2.*duration, 's'),
    #         self.animate('f_ilm', 'position_y', None, dest["y"], duration * 1/2, 's', easing),
    #         self.wait(duration, 's'),
    #
    #         self.trijc_change_tool('compas'),
    #         self.set(movie, 'video_time', 0),
    #         self.animate(movie, 'scale', None, [1.0, 1.0], zoom_duration, 's'),
    #         self.animate('f_arabesque_1', 'position_y', None, dest["y_arabesque"], zoom_duration, 's'),
    #         self.animate('f_arabesque_2', 'position_y', None, -dest["y_arabesque"], zoom_duration, 's'),
    #         self.signs_io('out', together=False, duration=complete_duration),
    #         self.wait(complete_duration / 2, 's'),
    #         self.animate('lights*', 'alpha', None, 0.3, complete_duration, 's', 'linear'),
    #         self.trijc_io('out', 'lustre', zoom_duration + 0.5)
    #     ])

########################## FILM

########################## JINGLES

    def jc_jingle_io(self, origin, duration, easing):
        """
        Having Jack Caesar Jingle dropping in / out
        """
        self.shaking_tv_jc()

        if origin == 'left':
            self.set('tv_jc', 'position', -1, 0, -12)
        elif origin == 'right':
            self.set('tv_jc', 'position', 1, 0, -12)
        elif origin == 'top':
            self.set('tv_jc', 'position', 0, 1, -12)
        elif origin == 'bottom':
            self.set('tv_jc', 'position', 0, -1, -12)
        else:
            self.logger.info('origine inconnue')

        self.start_scene('jack_caesar_jingle', lambda: [
            self.set('tv_jc', 'visible', 1),
            self.animate('tv_jc', 'position_x', None, 0.09, duration, 's', easing),
            self.animate('tv_jc', 'position_y', None, 0.01, duration / 2, 's', 'random'),
            self.wait(duration / 2, 's'),
            self.animate('tv_jc', 'position_y', None, 0.0, duration  / 2, 's', 'random'),
            self.wait(self.get('p_jc', 'video_end') - duration / 2, 's'),
            self.animate('tv_jc', 'position_x', None, 1, duration, 's', easing),
            self.animate('tv_jc', 'position_y', None, 0.01, duration / 2, 's', 'random'),
            self.wait(duration / 2, 's'),
            self.animate('tv_jc', 'position_y', None, 0.0, duration / 2, 's', 'random'),
            self.wait(duration / 2, 's'),
            self.stop_animate('plane_horn_jc', 'position_x'),
            self.stop_animate('plane_horn_jc', 'position_y'),
            self.stop_animate('p_jc', 'position_x'),
            self.stop_animate('p_jc', 'position_y'),
        ])

    def jc_jingle_in(self, origin, duration, easing):
        """
        Having Jack Caesar Jingle dropping in
        """
        self.shaking_tv_jc()

        if origin == 'left':
            self.set('tv_jc', 'position', -1, 0, -12)
        elif origin == 'right':
            self.set('tv_jc', 'position', 1, 0, -12)
        elif origin == 'top':
            self.set('tv_jc', 'position', 0, 1, -12)
        elif origin == 'bottom':
            self.set('tv_jc', 'position', 0, -1, -12)
        else:
            self.logger.info('origine inconnue')

        self.start_scene('jack_caesar_jingle', lambda: [
            self.set('tv_jc', 'visible', 1),
            self.animate('tv_jc', 'position_x', None, 0.09, duration, 's', easing),
            self.animate('tv_jc', 'position_y', None, 0.01, duration / 2, 's', 'random'),
            self.wait(duration / 2, 's'),
            self.animate('tv_jc', 'position_y', None, 0.0, duration  / 2, 's', 'random'),
        ])


########################## JINGLES

########################## Vanupiés Hacking
    def v_hackboat_io(self, direction='in', duration=1):
        """
        Hacking Vanupiés
        """
        pass
########################## Vanupiés Hacking

########################## METHODES GENERIQUES

    def shaking_slide(self, slide_name, property, range, duration = 1, easing = 'linear'):
        """
        To make a slide shake (by now not possible to send wildcard)
        """
        self.stop_animate(slide_name, property)
        center_value = self.get(slide_name, property)
        self.start_scene('sequence/shaking_' + slide_name + '_' + property, lambda: [
            self.animate(slide_name, property, None,  center_value - range / 2, duration / 2, 's', easing),
            self.wait(duration / 2, 's'),
            self.animate(slide_name, property, None, center_value + range / 2, duration, 's', easing + '-mirror', loop=True)
        ])


    def shaking_tvs(self, number, content):
        range_x = (_rand() / 2 + 0.5) * 0.01
        range_y = _rand() * 0.01
        duration = (_rand() / 2 + 0.5) * 10
        self.shaking_slide('plane_horn_' + str(number), 'position_x', range_x, duration)
        self.shaking_slide(content, 'position_x', range_x, duration)
        self.shaking_slide('plane_horn_' + str(number), 'position_y', range_y, duration, 'random')
        self.shaking_slide(content, 'position_y', range_y, duration, 'random')

    def shaking_tv_jc(self):
        range_x = (_rand() / 2 + 0.5) * 0.01
        range_y = _rand() * 0.01
        duration = (_rand() / 2 + 0.5) * 10
        self.shaking_slide('plane_horn_jc', 'position_x', range_x, duration)
        self.shaking_slide('p_jc', 'position_x', range_x, duration)
        self.shaking_slide('plane_horn_jc', 'position_y', range_y, duration, 'random')
        self.shaking_slide('p_jc', 'position_y', range_y, duration, 'random')

    def falldown(self, slide_name, chute, d):
        cur_y_pos = self.get(slide_name, 'position_y')
        self.start_scene('sequence/falldown_' + slide_name, lambda:[
            self.animate(slide_name, 'position_y', None, cur_y_pos - chute, 0.3, 's', 'elastic'),
            self.wait(0.3, 's'),
            self.animate(slide_name, 'position_y', None, cur_y_pos - chute + 0.001, 0.5, 's', 'random'),
            self.wait(0.5, 's'),
            self.animate(slide_name, 'position_y', None, cur_y_pos, d-0.8, 's', 'linear'),
            self.wait(d-0.8, 's'),
            ]
        )



########################## Routes

    def route(self, address, args):

        if address == '/pyta/subscribe/update' and args[0] == 'status':
            """
            if pyta is ready, query parameters for slides that are not ready
            """
            self.status = args[1]

        elif '/pyta/slide' in address and '/get/reply/end' in address:
            """
            if pyta a pyta slide has finished sending its parameters, it is ready
            """
            slide_name = address.split('/')[-4]
            self.submodules[slide_name].ready = True

        elif '/pyta/slide' in address and '/ping/reply' in address:
            """
            if pyta a pyta slide has finished sending its parameters, it is ready
            """
            slide_name = address.split('/')[-3]
            self.submodules[slide_name].ping = True


        elif '/pyta/slide' in address and '/get/reply' in address:
            """
            Handle feedback from slides
            """
            slide_name = address.split('/')[-3]

            if slide_name not in self.submodules:
                """
                Feedback from a new slide: create Slide object and query all parameters
                """
                slide = Slide(slide_name, parent=self)
                self.add_submodule(slide)

            else:
                """
                Feedback from existing slide: create parameter if it doesn't exist
                """
                slide = self.submodules[slide_name]
                property_name, *values = args
                if property_name not in slide.parameters and property_name not in self.get_excluded_parameters:

                    types = 's'
                    for v in values:
                        if type(v) == str:
                            types += 's'
                        else:
                            types += 'f'


                    slide.add_parameter(property_name, '/pyta/slide/%s/set' % slide_name, types=types, static_args=[property_name], default=values[0] if len(values) == 1 else values)
                    if property_name == 'scale':
                        slide.add_meta_parameter('zoom', ['scale'],
                            getter = lambda scale: scale[0],
                            setter = lambda zoom: slide.set('scale', zoom)
                        )

                    if property_name in ['position', 'rotate']:
                        axis = {0: '_x', 1: '_y', 2: '_z'}
                        for index, ax in axis.items():
                            def closure(index, ax):

                                def setter(val):
                                    value = slide.get(property_name)
                                    value[index] = val
                                    slide.set(property_name, *value, preserve_animation = True)

                                slide.add_meta_parameter(property_name + ax, [property_name],
                                    getter = lambda prop: prop[index],
                                    setter = setter
                                )

                            closure(index, ax)


        # Don't route message any further
        return False

    state_excluded_parameters = [
        'position_x',
        'position_y',
        'position_z',
        'rotate_x',
        'rotate_y',
        'rotate_z',
        'zoom',
        'ready'
    ]

    def get_state(self, *args, **kwargs):
        """
        Exclude some parameters from state
        """
        state = super(PytaVSL, self).get_state(*args, **kwargs)
        def filter_function(item):
            exclude = False
            for prop in self.state_excluded_parameters:
                if prop in item:
                    exclude = True
                    break
            return not exclude
        state = list(filter(filter_function, state))
        return state



    def is_ready(self):
        """
        Check if all Slide submodules are ready (meaning all their parameters are created)
        """
        for name in self.submodules:
            if not self.submodules[name].ready:
                return False
        return True

    def sync(self, timeout=5):
        """
        Wait until pyta and mentat are synced
        """
        timeleft = timeout
        step = 0.04
        self.logger.info('waiting for sync')
        while not self.is_ready():
            if self.status == 'ready':
                for name in self.submodules:
                    if not self.submodules[name].ready:
                        self.submodules[name].query_slide_state()

                timeout -= step
            elif self.status == 'loading':
                timeleft = timeout

            self.wait(step, 's')
            if timeleft < 0:
                self.logger.critical('could not sync with pyta (timed out, not ready: %s)' % [slide.name for slide in self.submodules.values() if not slide.ready])
        self.logger.info('sync ok')
