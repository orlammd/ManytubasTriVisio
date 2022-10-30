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
        self.ready = False
        self.status_locked = True
        self.pending_overlay = None

        # self.add_event_callback('parameter_changed', self.parameter_changed)


        # Objects JC Manytubas
        ### TODO -> à re-ranger de manière à factoriser trijc, t_trijc et ot_trijc
        self.m_TriJC = ['trijc_socle', 'trijc_tarte', 'trijc_head', 'trijc_souffle']
        self.t_TriJC = ['t_trijc_tuba', 't_trijc_aspi', 't_trijc_aimant', 't_trijc_compas']
        self.ot_TriJC = ['ot_trijc_taser']

        self.TriJC_xinpos = 0
        self.TriJC_xoutoffset = -0.3
        self.t_TriJC_xoffset = -0.415


###" A virer ?"
        # self.Tool_TriJC_xinpos = {
        #     "tuba": -0.415,
        #     "aspi": -0.415
        # }
        # self.Tool_TriJC_zoom = {
        #     "tuba": 1,
        #     "aspi": 1.185
        # }
        # self.Tool_TriJC_yinpos = {
        #     "tuba": -0.455,
        #     "aspi": -0.455
        # }
###" A virer ?"

        self.get_excluded_parameters = [
            'position_x',
            'position_y',
            'position_z',
            'rotate_x',
            'rotate_y',
            'rotate_z',
            'zoom'
        ]


        """
        PytaVSL reset
        """
        # remove all slides
        self.send('/pyta/slide/*/remove')

        # start pinging for new slides
        self.start_scene('check_new_slides', self.check_new_slides)

        # internal ready parameter (bool)
        # set to False when a new slide is created
        # set to True when no new parameter was added for a while
        self.add_parameter('ready', None, '*', default=False)
        self.feedback_counter = 0
        self.start_scene('check_ready_state', self.check_ready_state)



    def create_clone(self, src, dest):
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

        if slide_name not in self.submodules:
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


############################## A virer

    # def sset_prop(self, name, property, args):
    #     #### ORL TODO -> remplacer par set
    #     self.send('/pyta/slide/' + name + '/set', property, *args)
    #
    # def sanimate(self, name, property, start, end, duration, division, easing):
    #     self.send('/pyta/slide' + name + '/animate', property, start, end, duration, easing)
    #
    # def sanimate_prop(self, name, property, args):
    #     ### ORL TODO -> remplacer par animate
    #     # if isinstance(args[len(args) - 1], str):
    #     #     duration = args[len(args)- 2]
    #     # elif isinstance(args[len(args) - 1], int) or isinstance(args[len(args) -1], float):
    #     #     duration = args[len(args) - 1]
    #
    #     # self.logger.info('Durée' + str(duration))
    #
    #     self.send('/pyta/slide/' + name + '/animate', property, *args)
    #     # self.scene_start('wait_until_animate_finished', lambda: [
    #     #     self.wait(duration, 's'),
    #     #     self.set(name, property, *args)
    #     # ])
    #
#############################"" Fin à virer


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
            if 't_trijc_' in slide_name:
                if self.get(slide_name, 'visible'):
                    init_tool = slide_name

        self.start_scene('changing_tool', lambda: [
            self.animate(init_tool, 'rotate_z', None, 90, 0.1, 's'),
            self.wait(0.1, 's'),
            self.animate('t_trijc_' + end_tool, 'rotate_z', 90, 0, 0.2, 's', 'elastic-inout'),
            self.set(init_tool, 'visible', 0),
            self.set('t_trijc_' + end_tool, 'visible', 1),
        ])


    def aspi_slide(self, slide_name, warp_1, warp_4, duration):
        """
        Aspire une slide ou plusieurs slides dans l'aspi de trijc
        """
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
        ])

########################## TRIJC

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



########################## METHODES GENERIQUES

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

        climax_y = 0.3
        etape_zoom = 0.4 * dest["zo"]
        move_duration= 3/4 * duration
        zoom_duration = (1 - move_duration) * duration
        self.start_scene('sequences/miraye_in', lambda:[
            self.set(filename, 'video_time', 0),
            self.set(filename, 'video_speed', 1),
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

    def miraye_out(self, duration, easing):
        """
        Having Miraye Leparket stopping her storytelling
        """
        pass

########################## Miraye

########################## FILM

    def movie_in(self, duration, easing):
        """
        Having Moving coming to front
        """
        pass

    def movie_out(self, duration, easing):
        """
        Having Movie going back
        """
        pass

    def movie_split(self, splitmode, number, duration, easing):
        """
        Having several movies being split over the screen
        """
        pass

########################## FILM

########################## JINGLES

    def jcJingle_in(self, origin, duration, easing):
        """
        Having Jack Caesar Jingle dropping in
        """
        pass

    def jcJingle_out(self, destination, duration, easing):
        """
        Having Jack Caesar Jingle dropping out
        """
        pass

########################## JINGLES


##########################  A virer ?
    def get_slide_property(self, slide_name, property):
        if slide_name in self.submodules:
            return self.get(slide_name, property)

########################## A virer ?


########################## Get, set, overlay
    def check_new_slides(self, once=False):
        """
        Ping for new slides
        """
        if once:
            self.send('/pyta/slide/*/get', 'visible', self.engine.port)
        else:
            while True:
                self.check_new_slides(True)
                self.wait(1, 's')


    def check_ready_state(self):
        """
        Check how many feedback messages were received recently and change ready state accordingly
        (no message = ready)
        """
        last_count = 0
        while True:
            self.wait(1, 's')
            if self.feedback_counter == last_count:
                # no feedback for 1 second -> ready
                self.set('ready', True)
                self.feedback_counter = last_count = 0
            last_count = self.feedback_counter
########################## Get, set, overlay

########################## Routes



    def route(self, address, args):

        if address == '/pyta/subscribe/update' and args[0] == 'status':
            """
            If pyta is loading new slides, set ready to False,
            if pyta is ready, ping for new sldes
            """
            if args[1] == 'loading':
                self.set('ready', False)
                self.feedback_counter += 1
            elif args[1] == 'ready':
                self.check_new_slides(once=True)

        elif '/pyta/slide' in address and '/get/reply' in address:
            """
            Handle feedback from slides
            """
            slide_name = address.split('/')[-3]

            if slide_name not in self.submodules:
                """
                Feedback from a new slide: create Slide object and query all parameters
                """
                self.set('ready', False)
                self.feedback_counter += 1

                slide = Slide(slide_name, parent=self)
                self.add_submodule(slide)
                self.send('/pyta/slide/%s/get' % slide_name, '*', self.engine.port)

            else:
                """
                Feedback from existing slide: create parameter if it doesn't exist
                """
                slide = self.submodules[slide_name]
                property_name, *values = args
                if property_name not in slide.parameters and property_name not in self.get_excluded_parameters:
                    self.set('ready', False)
                    self.feedback_counter += 1

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
