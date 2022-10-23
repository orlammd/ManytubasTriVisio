from .keyboard import Keyboard


class JmjKeyboard(Keyboard):
    """
    Jean-Michel Jarring Effects & Planche à Touches Incorporated (mididings patch)
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.set_sound('ZDupieux')

    def route(self, address, args):
        if address == '/pedalVolume':
            self.logger.info('Volume Pedal: %i' % args[0])
