from mentat import Module

class Strip(Module):
    """
    NonMixer Strip
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

class Plugin(Module):
    """
    NonMixer Plugin
    """
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

class NonMixer(Module):
    """
    Base module for NonMixer instances.
    Retrieves all controllable parameters with their values automatically at init, structured as follows:
    NonMixer > Strips > Plugins > Parameters
    """

    def __init__(self, *args, **kwargs):

        Module.__init__(self, *args, **kwargs)

        self.signals = {}
        self.init_params = []

        # get submodules
        self.send('/non/hello', 'osc.udp://127.0.0.1:%i' % self.engine.port, '', '', self.engine.name)
        self.send('/signal/list')

    def route(self, address, args):
        """
        Populate submodules and parameters from non's response
        """

        if address == '/reply' and args[0] == '/signal/list':

            if len(args) > 1:
                """
                Populating
                """

                path = args[1].split('/')

                if path[1] == 'strip':

                    strip_name = path[2]

                    if strip_name not in self.submodules:

                        self.add_submodule(Strip(strip_name, parent=self))


                    strip_mod = self.submodules[strip_name]

                    if path[-1] == 'unscaled':

                        parameter_name = '/'.join(path[3:-1])
                        parameter_address = ('Non-Mixer.%s' % self.name) + '/' + '/'.join(path[1:])

                        plugin_name, _, param_shortname = parameter_name.partition('/')

                        if plugin_name in NonMixer.plugin_aliases:
                            plugin_name = NonMixer.plugin_aliases[plugin_name]
                        if param_shortname in NonMixer.parameter_aliases:
                            param_shortname = NonMixer.parameter_aliases[param_shortname]

                        if plugin_name not in strip_mod.submodules:
                            strip_mod.add_submodule(Plugin(plugin_name, parent=strip_mod))

                        plugin_mod = strip_mod.submodules[plugin_name]


                        plugin_mod.add_parameter(param_shortname, parameter_address, 'f', default=None)
                        plugin_mod.parameters[param_shortname].range = args[3:5]

                        self.init_params.append(parameter_address)

                        # self.submodules[strip_name].add_alias_parameter(NonMixer.plugin_aliases[plugin_name] + '/' + param_shortname , parameter_name)


            else: # only 1 arg: list end
                """
                All received, query current values and create meta parameters
                """
                for parameter_address in self.init_params:
                    self.send(parameter_address)


                self.create_meta_parameters()

        elif address == '/reply' and args[0] in self.init_params:
            path = args[0].partition('/strip/')[2]
            strip, _, pname = args[0].partition('/strip/')[2].partition('/')
            if 'unscaled' in pname:
                pname = pname[:-9]
            plugin_name, _, param_shortname = pname.partition('/')
            if plugin_name in NonMixer.plugin_aliases:
                plugin_name = NonMixer.plugin_aliases[plugin_name]
            if param_shortname in NonMixer.parameter_aliases:
                param_shortname = NonMixer.parameter_aliases[param_shortname]
            self.set(strip, plugin_name, param_shortname, args[1])
            self.init_params.remove(args[0])
            # self.logger.info('init parameter %s %s to value %s ' % (strip, pname, args[1]))

        return False

    def create_meta_parameters(self):
        """
        For specific instances we'll create meta parameters
        """
        pass

    # plugin_aliases = {
    #     'C%2A%20Scape%20-%20Stereo%20delay%20with%20chromatic%20resonances': 'Scape',
    #
    #     '4%20Pole%20Low-Pass%20Filter%20with%20Resonance%20(FCRCIA)': 'Lowpass',
    #     'AM%20pitchshifter': 'Pitchshifter'
    # }
    #
    # parameter_aliases = {
    #     'Gain%20(dB)': 'Gain',
    #
    #     'Cutoff%20Frequency': 'Cutoff', # 4 poles lowpass
    #     'Pitch%20shift': 'Pitch'
    # }
