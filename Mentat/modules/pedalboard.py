from mentat import Module

class PedalBoard(Module):
    """
    Pedalboard controller
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.route_select = False

        self.route_map = {
            1: 'Snapshat'
        }


    def route(self, address, args):
        """
        Let /pedaboard/button messages pass, unless we're in route selection mode (toggle with button 12)
        """

        if args[0] == 12:

            self.route_select = not self.route_select

            if self.route_select:
                self.logger.info('switched to route selection mode')
            else:
                self.logger.info('switched normal mode')

            return False # bypass further routing

        elif self.route_select:

            if args[0] in self.route_map:
                self.engine.set_route(self.route_map[args[0]])
            else:
                self.logger.info('no route in map for button %i' % args[0])

            self.route_select = False

            return False # bypass further routing

        else:
            pass
