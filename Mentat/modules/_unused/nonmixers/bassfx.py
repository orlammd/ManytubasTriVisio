from ..nonmixer import NonMixer

class BassFX(NonMixer):

    def create_meta_parameters(self):

        for strip_name in self.submodules:

            if not strip_name.endswith('In'):

                def closure(strip_name):

                    metaparam_name = strip_name[4:].lower() # remove "Bass" prefix

                    def getter(mute_in, mute):
                        if mute_in == 0.0 and mute == 0.0:
                            return 'on'
                        elif mute_in == 1.0 and mute == 1.0:
                            return 'off'
                        elif mute_in == 1.0 and mute == 0.0:
                            return 'preon'
                        elif mute_in == 0.0 and mute == 1.0:
                            return 'poston'
                        else:
                            return '?'

                    def setter(state):
                        if state == 'on':
                            self.set(strip_name + 'In', 'Gain', 'Mute', 0.0)
                            self.set(strip_name, 'Gain', 'Mute', 0.0)
                        elif state ==  'off':
                            self.set(strip_name + 'In', 'Gain', 'Mute', 1.0)
                            self.set(strip_name, 'Gain', 'Mute', 1.0)
                        elif state == 'preon':
                            self.set(strip_name + 'In', 'Gain', 'Mute', 0.0)
                            self.set(strip_name, 'Gain', 'Mute', 1.0)
                        elif state == 'poston':
                            self.set(strip_name + 'In', 'Gain', 'Mute', 1.0)
                            self.set(strip_name, 'Gain', 'Mute', 0.0)

                    self.add_meta_parameter(
                        metaparam_name,
                        [[strip_name + 'In', 'Gain', 'Mute'], [strip_name, 'Gain', 'Mute']],                                                   # params
                        getter, setter
                    )

                closure(strip_name)
