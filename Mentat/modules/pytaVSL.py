from mentat import Module
from random import randint
from os import listdir as _ls

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

        self.slides = []

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


        # if self.name == 'ProdSampler':
        #     self.add_parameter('kit', '/kit/select', 's', default='s:Snapshat')
        #     self.send('/setup/get/kits_list', 'Plagiat')

        ### TODO - récupérer liste calques
        #self.send('')


    def load_slide(self, f):
        """
        Chargement + Suivi d'un nouveau calques
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
            for param in ['visible', 'position_x', 'position_y', 'rotate_x', 'rotate_y', 'rotate_z', 'scale_x', 'scale_y']:
                slide.add_parameter(param, None, 'i', default=0)
                self.send('/pyta/slide/' + slide_name + '/get', param, 2001)
            # ORL -> vérifier pour position/rotate vs [x, y, z], zoom vs scale...
            if f.endswith('.mp4'):
                for vparam in ['video_time', 'video_speed', 'video_loop', 'video_end']:
                    slide.add_parameter(vparam, None, 'f', default=0)
                    self.send('/pyta/slide/' + slide_name + '/get', vparam, 2001)

            # populating





    def load_slides_from_dir(self, dir='Common'):
        """
        Chargement des calques
        """

        self.logger.info('load slides from dir: ' + dir)
        path_to_pyta = '/home/jeaneudes/OrageOTournage/ManytubasTriVisio/PytaVSL'

        if dir == 'Common':
            for d in _ls(path_to_pyta + '/' + dir):
                filelist = _ls(path_to_pyta + '/' + dir + '/' + d)
                for f in filelist:
                    self.load_slide(dir + "/" + d + "/" + f)
        else:
            filelist = _ls(path_to_pyta + '/' + dir)
            for f in filelist:
                self.load_slide(dir + "/" + f)

        # if chapter=='common':
        #     ## Fond
        #     self.send('/pyta/load', 'Common/Back/Back.png')
        #
        #     ## Lumières
        #     self.send('/pyta/load', 'Common/Lights/*')
        #
        #     ## Panneaux MANYTUBAS
        #     self.send('/pyta/load', 'Common/Signs/*')
        #
        #     ## Jack Caesar Automate
        #     self.send('/pyta/load', 'Common/TriJC/*')
        #
        # else:
        #     self.send('/pyta/load', chapter + '/*')


    def position_overlay(self):
        """
        Position des éléments de décor
        """

        self.logger.info('positionning overlay')

        ## Fond
        self.send('/pyta/slide/back/set', 'visible', 1)
        self.send('/pyta/slide/back/set', 'position', 0, 0, 100)

        ## Lights
        self.send('/pyta/slide/lights_stageleft/set', 'visible', 1)
        self.send('/pyta/slide/lights_stageleft/set', 'position', 0, 0, -20)
        self.send('/pyta/slide/lights_stageright/set', 'visible', 1)
        self.send('/pyta/slide/lights_stageright/set', 'position', 0, 0, -20.1)

        ## Panneaux Manytubas
        #### Clone des barres de maintien
        for sign in ['jack', 'caesar', 'manytubas', 'tri', 'visio']:
            self.send('/pyta/clone', 'signs_standleft_jack', 'signs_standright_' + sign)

            if not sign == 'jack':
                self.send('/pyta/clone', 'signs_standleft_jack', 'signs_standleft_' + sign)

            if sign == 'manytubas':
                self.send('/pyta/clone', 'signs_standleft_jack', 'signs_standcenter_' + sign)
                self.send('/pyta/slide/signs_standcenter_' + sign + '/set', 'rotate_z', randint(-30, 30))

            self.send('/pyta/slide/signs_standleft_' + sign + '/set', 'rotate_z', randint(-30, 30))
            self.send('/pyta/slide/signs_standright_' + sign + '/set', 'rotate_z', randint(-30, 30))

        #### Scaling des barres de maintien
        self.send('/pyta/slide/signs_stand*/set', 'zoom', 0.05)

        stands_hpos = 0.5
        #### Positionnement
        self.send('/pyta/slide/signs_jack/set', 'position', 0, 0, -19.1)
        self.send('/pyta/slide/signs_standleft_jack/set', 'position', -0.35, stands_hpos, -19.01)
        self.send('/pyta/slide/signs_standright_jack/set', 'position', -0.3, stands_hpos, -19.02)

        self.send('/pyta/slide/signs_caesar/set', 'position', 0, 0, -19.2)
        self.send('/pyta/slide/signs_standleft_caesar/set', 'position', -0.24, stands_hpos, -19.03)
        self.send('/pyta/slide/signs_standright_caesar/set', 'position', -0.17, stands_hpos, -19.04)

        self.send('/pyta/slide/signs_manytubas/set', 'position', 0, 0, -19.3)
        self.send('/pyta/slide/signs_standleft_manytubas/set', 'position', -0.11, stands_hpos, -19.03)
        self.send('/pyta/slide/signs_standcenter_manytubas/set', 'position', -0.02, stands_hpos, -19.04)
        self.send('/pyta/slide/signs_standright_manytubas/set', 'position', 0.075, stands_hpos, -19.04)

        self.send('/pyta/slide/signs_tri/set', 'position', 0, 0, -19.4)
        self.send('/pyta/slide/signs_standleft_tri/set', 'position', 0.16, stands_hpos, -19.03)
        self.send('/pyta/slide/signs_standright_tri/set', 'position', 0.19, stands_hpos, -19.04)

        self.send('/pyta/slide/signs_visio/set', 'position', 0, 0, -19.5)
        self.send('/pyta/slide/signs_standleft_visio/set', 'position', 0.24, stands_hpos, -19.03)
        self.send('/pyta/slide/signs_standright_visio/set', 'position', 0.3, stands_hpos, -19.04)

        self.send('/pyta/slide/signs_*/set', 'visible', 1)


        ## Jack Caesar Automate
        self.sset_prop('TriJC_*', 'visible', [1])
        i = 0
        for s in self.m_TriJC:
            self.sset_prop(s, 'position', [self.TriJC_xinpos + self.TriJC_xoutoffset, 0, -15 - i])
            i = i + 0.1

        i = 0
        for tool in ['Tuba', 'Aspi']:
            self.sset_prop('t_TriJC_' + tool, 'position', [self.Tool_TriJC_xinpos[tool] + self.TriJC_xoutoffset, self.Tool_TriJC_yinpos[tool], -16 - i])
            self.sset_prop('t_TriJC_' + tool, 'zoom', [self.Tool_TriJC_zoom[tool]])
            self.sset_prop('t_TriJC_' + tool, 'visible', [1])
            i = i + 0.1

        # self.sset_prop('TriJC_Tarte', 'position', [0, 0, -15.1])
        # self.sset_prop('TriJC_Head', 'position', [0, 0, -15.2])
        # self.sset_prop('TriJC_Tuba', 'position', [0, 0, -15.3])


    def sset_prop(self, name, property, args):
        #### ORL TODO -> remplacer par set
        self.send('/pyta/slide/' + name + '/set', property, *args)

    def sanimate_prop(self, name, property, args):
        ### ORL TODO -> faire un set à la fin de l'animate
        self.send('/pyta/slide/' + name + '/animate', property, *args)

    def trijc_io(self, direction='in', tool="Tuba", duration=0.5, easing='linear'):
        s = "TriJC_*"

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
