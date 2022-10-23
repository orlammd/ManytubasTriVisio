from mentat import Module
import fnmatch


class PostProcess(Module):
    """
    Post processing effects managers for main mix outputs (bass, synths, samples, vocals)
    """


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.no_AMpitch = ['VocalsNano', 'VocalsKesch']


    def set_pitch(self, strip_name, pitch):
        """
        Set pitch shifting parameter for one or multiple strips.
        For vocals this is handled at the autotuner's level, for the others with AM Pitchshifter

        **Parameters**

        - `strip_name`: name of strip (with unix filename pattern matching support), or list of names
        - `pitch`: pitch multiplier (0.5 = -1 octave, 2 = +1 octave)
        """
        if type(strip_name) is list:
            for n in strip_name:
                self.set_pitch(n, pitch)
            return

        mod = self.engine.modules['Outputs']

        for n in fnmatch.filter(mod.submodules.keys(), strip_name):
            if n not in self.no_AMpitch:
                if 'Pitchshifter' in mod.submodules[n].submodules:
                    mod.set(n, 'Pitchshifter', 'Pitch', pitch)
            else:
                pre = n[6:]
                for name in [pre+'Meuf', pre+'Normo', pre+'Gars']:
                    self.engine.modules[name].set('pitch', pitch)

    def animate_pitch(self, strip_name, start, end, duration, mode='beats', easing='linear'):
        """
        Animate pitch shifting for one or multiple strips

        **Parameters**

        - `strip_name`: name of strip (with unix filename pattern matching support), or list of names
        - `start`: pitch multiplier start value (0.5 = -1 octave, 2 = +1 octave)
        - `end`: pitch multiplier end value (0.5 = -1 octave, 2 = +1 octave)
        - `duration`: animation duration
        - `mode`: beats or seconds
        - `easing`: interpolation curve (see mentat's documentation)
        """
        if type(strip_name) is list:
            for n in strip_name:
                self.animate_pitch(n, start, end, duration, mode, easing)
            return

        mod = self.engine.modules['Outputs']
        for n in fnmatch.filter(mod.submodules.keys(), strip_name):
            if n not in self.no_AMpitch:
                if 'Pitchshifter' in mod.submodules[n].submodules:
                    mod.animate(n, 'Pitchshifter', 'Pitch', start, end, duration, mode, easing)
            else:
                pre = n[6:]
                for name in [pre+'Meuf', pre+'Normo', pre+'Gars']:
                    self.engine.modules[name].animate(n, 'Pitch', start, end, duration, mode, easing)


    def set_filter(self, strip_name, freq):
        """
        Set lowpass filter cutoff parameter for one or multiple strips, or list of names

        **Parameters**

        - `strip_name`: name of strip (with unix filename pattern matching support)
        - `freq`: cutoff frequency in Hz
        """
        if type(strip_name) is list:
            for n in strip_name:
                self.set_filter(n, freq)
            return

        mod = self.engine.modules['Outputs']
        for n in fnmatch.filter(mod.submodules.keys(), strip_name):
            if 'Lowpass' in mod.submodules[n].submodules:
                mod.set(n, 'Lowpass', 'Cutoff', freq)

    def animate_filter(self, strip_name, start, end, duration, mode='beats', easing='linear'):
        """
        Animate lowpass filter cutoff for one or multiple strips

        **Parameters**

        - `strip_name`: name of strip (with unix filename pattern matching support), or list of names
        - `start`: cutoff frequency start value in Hz
        - `end`: cutoff frequency end value in Hz
        - `duration`: animation duration
        - `mode`: beats or seconds
        - `easing`: interpolation curve (see mentat's documentation)
        """
        if type(strip_name) is list:
            for n in strip_name:
                self.animate_filter(n, start, end, duration, mode, easing)
            return
        mod = self.engine.modules['Outputs']
        for n in fnmatch.filter(mod.submodules.keys(), strip_name):
            if 'Lowpass' in mod.submodules[n].submodules:
                mod.animate(n, 'Lowpass', 'Cutoff', start, end, duration, mode, easing)


    def slice(self):
        pass

    def animate_slice(self):
        pass
