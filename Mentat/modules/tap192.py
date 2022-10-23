from mentat import Module

class Tap192(Module):
    """
    Sample player
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.kits = []

        self.ready = False
        self.pending_kit = None

        if self.name == 'ProdSampler':
            self.add_parameter('kit', '/kit/select', 's', default='s:Snapshat')
            self.send('/setup/get/kits_list', 'Plagiat')

    def set_kit(self, name):
        """
        Set active kit by name

        **Parameters**

        - `name`: name of kit (as written in Tap192)
        """

        if self.ready:

            if name in self.kits:

                name = 's:' + name
                self.set('kit', name, force_send=True)
                self.logger.info('switched to kit %s' % name)

            else:

                self.logger.error('kit %s not found' % name)

        else:

            self.pending_kit = name
            self.logger.info('not ready yet: set_kit() call deffered')


    def route(self, address, args):
        """
        Store kit list sent by Tap192
        """
        if address == '/setup/tap192/kits_list':

            self.kits = args[1:]

            if not self.ready:
                self.ready = True
                if self.pending_kit:
                    self.logger.info('ready now: calling set_kit()')
                    self.set_kit(self.pending_kit)

        return False
