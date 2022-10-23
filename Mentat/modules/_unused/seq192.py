from mentat import Module

class Seq192(Module):
    """
    Seq192 Midi sequencer
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.add_parameter('tempo', '/bpm', 'f', default=120)
        self.add_parameter('screenset', '/screenset', 'i', default=0)

        self.screenset_map = {
            'Snapshat': 0,
            'Mcob': 1,
            'AgneauGastrik': 2,
            'SaperComJaja': 3,
            'Stagiaire' : 4,
            'SW': 5,
            'ViktorHuguau' : 6,
            'RamenerMooncup': 7
        }

    def start(self):
        """
        Start playback
        """
        self.send('/play')

    def stop(self):
        """
        Stop playback
        """
        self.send('/stop')

    def set_screenset(self, name):
        """
        Set active screenset by name.

        **Parameters**

        - `name`: screenset name
        """
        if name in self.screenset_map:
            self.set('screenset', self.screenset_map[name], force_send=True)
        else:
            self.logger.error('screenset %s not found' % name)

    def select(self, *args):
        """
        Set sequence(s) state.

        selet(mode, colum)
        selet(mode, colum, *row)
        selet(mode, *name)

        **Parameters**

        - `mode`:
            - "solo", "on", "off", "toggle", "record", "record_on", "record_off", "clear"
            - only one sequence can be recording at a time
            - "record_off" mode doesn't require any argument
        - `column`: column number on active screenset (0-indexed)
        - `*row`:
            - row number(s) on active screenset (0-indexed)
            - multiple rows can be specified
            - if omitted, all rows are affected
        - `*name`:
            - sequence name or osc pattern (can match multiple sequence names)
            - multiple names can be specified
        """
        self.send('/sequence', *args)
