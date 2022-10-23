from mentat import Module

class PytaVSL(Module):
    """
    VJing Producer
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.slides = []

        # if self.name == 'ProdSampler':
        #     self.add_parameter('kit', '/kit/select', 's', default='s:Snapshat')
        #     self.send('/setup/get/kits_list', 'Plagiat')

        ### TODO - récupérer liste calques
        #self.send('')


        ## UTILE ?
    # def route(self, address, args):
    #     """
    #     Store slides list sent by pytaVSL
    #     """
    #     if address == '/setup/pytaVSL/slides_list':
    #         self.slides = args[1:]
    #    return False

    def miraye_in(self, duration, easing):
        """
        Having Miraye Leparket starting her storytelling
        """
        pass

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
