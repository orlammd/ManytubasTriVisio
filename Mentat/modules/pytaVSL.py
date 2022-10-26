from mentat import Module
from random import randint
from os import listdir as _ls
import toml

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
        self.m_TriJC = ['TriJC_Socle', 'TriJC_Tarte', 'TriJC_Head']
        # self.w_TriJC = ['TriJC_Socle', 'TriJC_Tarte', 'TriJC_Head', 'TriJC_Tuba']

        self.TriJC_xinpos = 0
        self.TriJC_xoutoffset = -0.3

        self.Tool_TriJC_xinpos = {
            "Tuba": -0.415,
            "Aspi": -0.415
        }
        self.Tool_TriJC_zoom = {
            "Tuba": 1,
            "Aspi": 1.185
        }
        self.Tool_TriJC_yinpos = {
            "Tuba": -0.455,
            "Aspi": -0.455
        }


    def parameter_changed(self, module, name, value):
        if name in ['position', 'rotate']:
            i = 0
            for axe in ['_x', '_y', '_z']:
                if axe == '_z':
                    pass
                else:
                    self.set(module.name, name + axe, value[i])
                    i = i+1
        elif name == 'zoom':
            self.set(module.name, 'scale', value[0], value[0])

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
            #self.logger.info('file ' + f + ' in new slide: ' + slide_name)
            slide = Slide(slide_name, parent=self)

            self.add_submodule(slide)
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
                # content = ''
                # for line in _content.split('\n'):
                #     if '=' in line:
                #         line += ']'
                #     content += line + '\n'
                # content = content.replace('=', '= [')
                scene = toml.loads(_content)
                self.logger.info('Fichier lu')

                for slide in self.submodules:
                    if slide.lower() in scene['slides']:
                        for param in self.slide_params:
                            self.logger.info(slide + "/" + param)
                            if param in scene['slides'][slide.lower()]:
                                param_value = scene['slides'][slide.lower()][param]
                                if len(param_value) == 1:
                                    self.set(slide, param, param_value[0])
                                elif len(param_value) == 2:
                                    self.set(slide, param, param_value[0], param_value[1])
                                elif len(param_value) == 3:
                                    self.set(slide, param, param_value[0], param_value[1], param_value[2])



            except Exception as e:
                self.logger.error('could not load scene file in dir %s' % overlay)



        else:
            self.pending_overlay = overlay
            self.logger.info('not ready yet: position_overlay() call deffered')


    def sset_prop(self, name, property, args):
        #### ORL TODO -> remplacer par set
        self.send('/pyta/slide/' + name + '/set', property, *args)

    def sanimate_prop(self, name, property, args):
        ### ORL TODO -> faire un set à la fin de l'animate
        self.send('/pyta/slide/' + name + '/animate', property, *args)

    def trijc_io(self, direction='in', tool="Tuba", duration=0.5, easing='linear'):
        s = "TriJC_*"
        xoffset = -0.3

        if direction == 'in':
            end = self.TriJC_xinpos
            start = end + self.TriJC_xoutoffset

            t_end = self.Tool_TriJC_xinpos[tool]
            t_start = t_end + self.TriJC_xoutoffset
        elif direction == 'out':
            start = self.TriJC_xinpos
            end = start + self.TriJC_xoutoffset

            t_start = self.Tool_TriJC_xinpos[tool]
            t_end = t_start + self.TriJC_xoutoffset


        self.start_scene('sequences/triJC_io', lambda: [
            [self.sanimate_prop(s, 'position_x', [start, end, duration, easing]), self.sanimate_prop('t_TriJC_' + tool, 'position_x', [t_start, t_end, duration, easing])],
            [self.sanimate_prop(s, 'position_y', [0, 0.01, duration/2., 'random']), self.sanimate_prop('t_TriJC_' + tool, 'position_y', [self.Tool_TriJC_yinpos[tool], self.Tool_TriJC_yinpos[tool] + 0.01, duration/2., 'random'])],
            self.wait(duration/2., 's'),
            [self.sanimate_prop(s, 'position_y', [0.01, 0, duration/2., 'random']), self.sanimate_prop('t_TriJC_' + tool, 'position_y', [self.Tool_TriJC_yinpos[tool] + 0.01, self.Tool_TriJC_yinpos[tool], duration/2., 'random'])]
            ]
        )

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
            self.sanimate_prop('t_TriJC_Tuba', 'rotate_z', [0, -7, 0.4, 'elastic']),
            self.wait(0.4, 's'),
            [self.sset_prop('MirayeLayout', 'visible', [1]), self.sset_prop(filename, 'visible', [1])],
            [self.sanimate_prop('MirayeLayout', 'position_x', [orig["x"], dest["x"], duration*3/4., easing]),self.sanimate_prop(filename, 'position_x', [orig["x"], dest["x"] - 0.0005, duration*3/4., easing])],
            [self.sanimate_prop('MirayeLayout', 'rotate_z', [orig["rot"], dest["rot"], duration*3/4., easing]), self.sanimate_prop(filename, 'rotate_z', [orig["rot"], dest["rot"], duration*3/4., easing])],
            [self.sanimate_prop('MirayeLayout', 'zoom', [orig["zo"], dest["zo"]*0.8/2, duration*3/4., easing]), self.sanimate_prop(filename, 'zoom', [orig["zof"], dest["zof"]*0.8/2, duration*3/4., easing])],
            [self.sanimate_prop('MirayeLayout', 'position_y', [orig["y"], 0.3, duration*1/2., easing]), self.sanimate_prop(filename, 'position_y', [orig["y"], 0.3, duration*1/2., easing])],
            self.wait(1/2.*duration, 's'),
            [self.sanimate_prop('MirayeLayout', 'position_y', [0.3, dest["y"], duration*1/4., easing]), self.sanimate_prop(filename, 'position_y', [0.3, dest["y"], duration*1/4., easing])],
            self.wait(1/4.*duration, 's'),
            [self.sanimate_prop('MirayeLayout', 'zoom', [dest["zo"]*1/2., dest["zo"], duration/4, easing]), self.sanimate_prop(filename, 'zoom', [dest["zof"]*1/2., dest["zof"], duration/4, easing])], self.sanimate_prop('t_TriJC_Tuba', 'rotate_z', [-7, 0, 0.4, 'random']),
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
                self.logger.info(slide_name + ' / ' + args[0] + ': ' + str(self.get(slide_name, args[0])))

        if address == '/pyta/subscribe/update' and args[0]== 'status' and args[1] == 'ready':

            if not self.ready:
                self.ready = True

                if self.pending_overlay:
                    self.logger.info('ready now: calling position_overlay()')
                    self.position_overlay(self.pending_overlay)

        return False
