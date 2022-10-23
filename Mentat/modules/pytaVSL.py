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


        return False
