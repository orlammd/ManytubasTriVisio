from mentat import Module
from .keyboard import Keyboard


class Mk2Keyboard(Keyboard):
    """
    Mk2 piano keyboard (mididings patch)
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.set_sound('ZBombarde')


class Mk2Control(Module):
    """
    Mk2 MIDI control interface
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.sysex = []

        self.shift_key = False

    def set_lights(self, lights):
        """
        Generates sysex messages for setting colors on pads

        **Parameters**

        - `lights`:
            `dict` with pad number as keys (1-indexed) and color names as values. Omitted pad will be turned off.
            Available color: red, blue, green purple, cyan, yellow, white
        """
        self.logger.info('setting lights')
        self.sysex = []
        for i in range(1,17):
            color = self.default_colors[i-1]
            if i in lights:
                color = self.mk2colors['purple']
                if type(lights) == dict:
                    color =  self.mk2colors[lights[i]]
                elif i == 1:
                    color = self.mk2colors['blue']
                elif i == 8:
                    color = self.mk2colors['red']

            self.sysex.append([0xf0, 0x00, 0x20, 0x6b, 0x7f, 0x42, 0x02, 0x00, 0x10, 111 + i, color, 0xf7])

        self.resend_lights()

    def resend_lights(self):
        """
        Send sysex messages to mk2
        """

        for s in self.sysex:
            # self.logger.info('sending /sysex %s' % s)
            self.send('/sysex', *s)

    def route(self, address, args):
        """
        Route controls from mk2.
        Reset colors whenever a pad is hit, otherwise it dosen't stay lit.
        """
        #self.logger.info('%s %s' %(address, args))

        if self.shift_key:

            if address == '/pitch_bend':

                p = 1.0 + args[1] / 8192 * 0.75

                self.engine.modules['PostProcess'].set_pitch('*', p)


        if address == '/control_change':

            cc = args[1]
            if cc > 100 and cc < 117 and args[2] == 0:

                if cc < 109:
                    # pads 1-8
                    self.engine.route('osc', 'mk2', '/mk2/button', [cc - 100])
                else:
                    pass

                self.resend_lights()

        elif address == '/sysex':

            if args[:-2] == [240, 0, 32, 107, 127, 66, 2, 0, 0, 46]:
                self.shift_key = args[-2] == 127

        return False

    mk2colors = mk2colors = {
        'red': 1,
        'blue': 16,
        'green': 4,
        'purple': 17,
        'cyan': 20,
        'yellow': 5,
        'white': 127
    }

    default_colors = [
    	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # buttons 1-8
    	mk2colors['red'], mk2colors['red'],mk2colors['yellow'], # sl vx pre rec/overdub/pause
    	mk2colors['red'], mk2colors['red'],mk2colors['yellow'], # sl vx post rec/overdub/pause
    	0x00, mk2colors['purple']
    ]
