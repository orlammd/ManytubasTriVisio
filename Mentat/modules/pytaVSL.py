from mentat import Module
from random import randint

class PytaVSL(Module):
    """
    VJing Producer
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.slides = []

        # Objects JC Manytubas
        self.m_TriJC = ['TriJC_Socle', 'TriJC_Tarte', 'TriJC_Head']
        self.w_TriJC = ['TriJC_Socle', 'TriJC_Tarte', 'TriJC_Head', 'TriJC_Tuba']

        self.w_TriJC_outpos = -0.3
        self.w_TriJC_inpos = 0


        # if self.name == 'ProdSampler':
        #     self.add_parameter('kit', '/kit/select', 's', default='s:Snapshat')
        #     self.send('/setup/get/kits_list', 'Plagiat')

        ### TODO - récupérer liste calques
        #self.send('')


    def load_slides(self, chapter='common'):
        """
        Chargement des calques
        """
        if chapter=='common':
            ## Fond
            self.send('/pyta/load', 'Common/Back/Back.png')

            ## Lumières
            self.send('/pyta/load', 'Common/Lights/*')

            ## Panneaux MANYTUBAS
            self.send('/pyta/load', 'Common/Signs/*')

            ## Jack Caesar Automate
            self.send('/pyta/load', 'Common/TriJC/*')

        else:
            self.send('/pyta/load', chapter + '/*')


    def position_overlay(self):
        """
        Position des éléments de décor
        """
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
        self.sset_prop('TriJC_Socle', 'position', [0, 0, -15])
        self.sset_prop('TriJC_Tarte', 'position', [0, 0, -15.1])
        self.sset_prop('TriJC_Head', 'position', [0, 0, -15.2])
        self.sset_prop('TriJC_Tuba', 'position', [0, 0, -15.3])


        ## UTILE ?
    # def route(self, address, args):
    #     """
    #     Store slides list sent by pytaVSL
    #     """
    #     if address == '/setup/pytaVSL/slides_list':
    #         self.slides = args[1:]
    #    return False

    def sset_prop(self, name, property, args):
        self.send('/pyta/slide/' + name + '/set', property, *args)

    def sanimate_prop(self, name, property, args):
        self.send('/pyta/slide/' + name + '/animate', property, *args)

    def trijc_io(self, direction, duration=0.5, easing='linear'):
        s = "TriJC_*"
        if direction == 'in':
            end = self.w_TriJC_inpos
            start = self.w_TriJC_outpos
        elif direction == 'out':
            start = self.w_TriJC_inpos
            end = self.w_TriJC_outpos

        self.start_scene('sequences/triJC_io', lambda: [
            self.sanimate_prop(s, 'position_x', [start, end, duration, easing]),
            self.sanimate_prop(s, 'position_y', [0, 0.01, duration/2., 'random']),
            self.wait(duration/2., 's'),
            self.sanimate_prop(s, 'position_y', [0.01, 0, duration/2., 'random'])
            ]
        )

    def miraye_in(self, duration=1, easing='linear'):
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
            "rot": -130
        }
        dest = {
            "x": 0.092,
            "y": 0.016,
            "z": -10,
            "zo": 0.837,
            "rot": -720
        }

        self.start_scene('sequences/miraye_in', lambda:[
            self.sanimate_prop('MirayeLayout', 'position_x', [orig["x"], dest["x"], duration*3/4., easing]),
            self.sanimate_prop('MirayeLayout', 'rotate_z', [orig["rot"], dest["rot"], duration*3/4., easing]),
            self.sanimate_prop('MirayeLayout', 'zoom', [orig["zo"], dest["zo"]*0.8/2, duration*3/4., easing]),
            self.sanimate_prop('MirayeLayout', 'position_y', [orig["y"], 0.3, duration*1/2., easing]),
            self.wait(1/2.*duration, 's'),
            self.sanimate_prop('MirayeLayout', 'position_y', [0.3, dest["y"], duration*1/4., easing]),
            self.wait(1/4.*duration, 's'),
            self.sanimate_prop('MirayeLayout', 'zoom', [dest["zo"]*1/2., dest["zo"], duration/4, easing]),
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
