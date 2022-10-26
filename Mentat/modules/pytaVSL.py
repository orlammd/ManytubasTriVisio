from mentat import Module
from random import randint
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
            'video_time', 'video_speed', 'video_loop', 'video_end', 'rgbwave', 'noise', 'warp_1', 'warp_2', 'warp_3', 'warp_4']

        self.send('/pyta/subscribe', 'status', 2001)
        self.send('/pyta/subscribe', 'status', 23456)
        self.ready = False
        self.pending_overlay = None

        self.add_event_callback('parameter_changed', self.parameter_changed)


        # Objects JC Manytubas
        ### TODO -> à re-ranger de manière à factoriser trijc, t_trijc et ot_trijc
        self.m_TriJC = ['trijc_socle', 'trijc_tarte', 'trijc_head', 'trijc_souffle']
        self.t_TriJC = ['t_trijc_tuba', 't_trijc_aspi', 't_trijc_aimant', 't_trijc_compas']
        self.ot_TriJC = ['ot_trijc_taser']

        self.TriJC_xinpos = 0
        self.TriJC_xoutoffset = -0.3
        self.t_TriJC_xoffset = -0.415

        self.Tool_TriJC_xinpos = {
            "tuba": -0.415,
            "aspi": -0.415
        }
        self.Tool_TriJC_zoom = {
            "tuba": 1,
            "aspi": 1.185
        }
        self.Tool_TriJC_yinpos = {
            "tuba": -0.455,
            "aspi": -0.455
        }


    def parameter_changed(self, module, name, value):
        if name in ['position', 'rotate']:
            i = 0
            for axe in ['_x', '_y', '_z']:
                # if module.name == 'back':
                #     self.logger.info('Passage par parameter_changed: ' + module.name + ' / ' + name + axe)
                self.set(module.name, name + axe, value[i])
                i = i+1
        elif name == 'zoom':
            self.set(module.name, 'scale', value[0], value[0])


    def add_slide_and_params(self, slide_name):
        slide = Slide(slide_name, parent=self)

        self.add_submodule(slide)
        self.logger.info('Adding slide ' + slide_name + ' as a submodule')
        for param in self.slide_params:
            if param in ['position', 'rotate']:
                slide.add_parameter(param, None, 'sfff', [param])
            elif param in ['warp_1', 'warp_2', 'warp_3', 'warp_4', 'scale']:
                slide.add_parameter(param, '/pyta/slide/' + slide_name + '/set', 'sff', [param])
            elif param in ['zoom']:
                slide.add_parameter(param, None, 'sff', [param])
            else:
                slide.add_parameter(param, '/pyta/slide/' + slide_name + '/set', 'sf', [param])

            if param == 'video_end':
                self.send('/pyta/slide/' + slide_name + '/get', param, 2001)

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
            self.add_slide_and_params(slide_name)
            # slide = Slide(slide_name, parent=self)
            #
            # self.add_submodule(slide)
            # for param in self.slide_params:
            #     if param in ['position', 'rotate']:
            #         slide.add_parameter(param, None, 'sfff', [param])
            #     elif param in ['warp_1', 'warp_2', 'warp_3', 'warp_4', 'scale']:
            #         slide.add_parameter(param, '/pyta/slide/' + slide_name + '/set', 'sff', [param])
            #     elif param in ['zoom']:
            #         slide.add_parameter(param, None, 'sff', [param])
            #     else:
            #         slide.add_parameter(param, '/pyta/slide/' + slide_name + '/set', 'sf', [param])
            #
            #     if param == 'video_end':
            #         self.send('/pyta/slide/' + slide_name + '/get', param, 2001)



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





    def position_overlay(self, overlay='Common'):
        """
        Position des éléments de décor
        """

        if self.ready:

            try:
                _content = open(self.path_to_pyta + '/' + overlay + '/overlay', 'r').read()
                scene = toml.loads(_content)
                # firstpass = True
                for clone in scene['clones']:
                    # if firstpass:
                    #     self.logger.info(scene['clones'][clone]['target'][0])
                    #     firstpass = False
                    # self.logger.info(clone)
                    # self.logger.info(scene['clones'][clone]['target'][0])
                    self.send('/pyta/clone', scene['clones'][clone]['target'][0], clone)
                    time.sleep(0.1)
                    self.add_slide_and_params(clone)

                    # self.logger.info('Submodules list:')
                    # for sub in self.submodules:
                    #     self.logger.info(sub)

                for slide in self.submodules:
                    log = False
                    if slide.lower() in scene['slides']:
                        if slide.lower() == 'Dummy':
                            log = True
                            self.logger.info('Slide observé:' + slide)
                        for param in self.slide_params:
                            if log == True:
                                self.logger.info("Reading scene file : " + slide + "/" + param)
                            if param in scene['slides'][slide.lower()]:
                                param_value = scene['slides'][slide.lower()][param]
                                if len(param_value) == 1:
                                    self.set(slide, param, param_value[0], force_send=True)
                                    # if log == True:
                                    #     self.logger.info('value: ' + str(param_value[0]))
                                elif len(param_value) == 2:
                                    self.set(slide, param, param_value[0], param_value[1], force_send=True)
                                    if log == True:
                                        self.logger.info('values: ' + str(param_value[0]) + ", " + str(param_value[1]))
                                elif len(param_value) == 3:
                                    self.set(slide, param, param_value[0], param_value[1], param_value[2], force_send=True)
                                    # if log == True:
                                    #     self.logger.info('values: ' + str(param_value[0]) + ", " + str(param_value[1]) + ", " + str(param_value[2]))

            except Exception as e:
                self.logger.error('could not load scene file in dir %s' % overlay)

        else:
            self.pending_overlay = overlay
            self.logger.info('not ready yet: position_overlay() call deffered')


    def sset_prop(self, name, property, args):
        #### ORL TODO -> remplacer par set
        self.send('/pyta/slide/' + name + '/set', property, *args)

    def sanimate_prop(self, name, property, args):
        ### ORL TODO -> remplacer par animate
        if isinstance(args[len(args) - 1], str):
            duration = args[len(args)- 2]
        elif isinstance(args[len(args) - 1], int) or isinstance(args[len(args) -1], float):
            duration = args[len(args) - 1]

        self.logger.info('Durée' + str(duration))

        self.send('/pyta/slide/' + name + '/animate', property, *args)
        self.scene_start('wait_until_animate_finished', lambda: [
            self.wait(duration, 's'),
            self.set(name, property, *args)
        ])

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

    def miraye_in(self, filename, duration=1, easing='linear'):
        """
        Having Miraye Leparket starting her storytelling
        """
        ## TODO : vérifier si TriJC visible, sinon, le faire apparaître
        '''
            [orig, dest]: x, y, z, zoom, rotate_z
        '''
        orig = {
            "x": -0.41,
            "y": -0.01,
            "z": -10,
            "zo": 0.04,
            "zof": 0.035,
            "rot": -130
        }
        dest = {
            "x": 0.092,
            "y": 0.016,
            "z": -10,
            "zo": 0.837,
            "zof": 0.71,
            "rot": -720
        }

        self.sset_prop('MirayeLayout', 'position', [orig["x"], orig["y"], orig["z"]])
        self.sset_prop('MirayeLayout', 'zoom', [orig["zo"]])

        self.sset_prop(filename, 'position', [orig["x"], orig["y"], orig["z"] + 0.1])
        self.sset_prop(filename, 'zoom', [orig["zof"]])


        self.start_scene('sequences/miraye_in', lambda:[
            self.sset_prop(filename, 'video_speed', [1]),
            self.sset_prop(filename, 'video_time', [0]),
            self.sanimate_prop('t_trijc_tuba', 'rotate_z', [0, -7, 0.4, 'elastic']),
            self.wait(0.4, 's'),
            [self.sset_prop('MirayeLayout', 'visible', [1]), self.sset_prop(filename, 'visible', [1])],
            [self.sanimate_prop('MirayeLayout', 'position_x', [orig["x"], dest["x"], duration*3/4., easing]),self.sanimate_prop(filename, 'position_x', [orig["x"], dest["x"] - 0.0005, duration*3/4., easing])],
            [self.sanimate_prop('MirayeLayout', 'rotate_z', [orig["rot"], dest["rot"], duration*3/4., easing]), self.sanimate_prop(filename, 'rotate_z', [orig["rot"], dest["rot"], duration*3/4., easing])],
            [self.sanimate_prop('MirayeLayout', 'zoom', [orig["zo"], dest["zo"]*0.8/2, duration*3/4., easing]), self.sanimate_prop(filename, 'zoom', [orig["zof"], dest["zof"]*0.8/2, duration*3/4., easing])],
            [self.sanimate_prop('MirayeLayout', 'position_y', [orig["y"], 0.3, duration*1/2., easing]), self.sanimate_prop(filename, 'position_y', [orig["y"], 0.3, duration*1/2., easing])],
            self.wait(1/2.*duration, 's'),
            [self.sanimate_prop('MirayeLayout', 'position_y', [0.3, dest["y"], duration*1/4., easing]), self.sanimate_prop(filename, 'position_y', [0.3, dest["y"], duration*1/4., easing])],
            self.wait(1/4.*duration, 's'),
            [self.sanimate_prop('MirayeLayout', 'zoom', [dest["zo"]*1/2., dest["zo"], duration/4, easing]), self.sanimate_prop(filename, 'zoom', [dest["zof"]*1/2., dest["zof"], duration/4, easing])], self.sanimate_prop('t_trijc_tuba', 'rotate_z', [-7, 0, 0.4, 'random']),
        ])


    def miraye_out(self, duration, easing):
        """
        Having Miraye Leparket stopping her storytelling
        """
        pass

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

    def get_slide_property(self, slide_name, property):
        if slide_name in self.submodules:
            return self.get(slide_name, property)

    def route(self, address, args):
        if address.startswith('/pyta/slide') and address.endswith('/reply'):
            slide_name = address.partition('/pyta/slide/')[2].partition('/')[0]

            if slide_name in self.submodules:
                self.set(slide_name, args[0], args[1])
                # self.logger.info(slide_name + ' / ' + args[0] + ': ' + str(self.get(slide_name, args[0])))

        if address == '/pyta/subscribe/update' and args[0]== 'status' and args[1] == 'ready':
            if not self.ready:
                self.ready = True

                if self.pending_overlay:
                    self.logger.info('ready now: calling position_overlay()')
                    self.position_overlay(self.pending_overlay)



        return False
