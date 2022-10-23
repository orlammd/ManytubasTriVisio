from ..nonmixer import NonMixer

class Vocals(NonMixer):

    def create_meta_parameters(self):

        strip_prefix = self.name[6:] # remove "Vocals" prefix

        for name in ['normo', 'gars', 'meuf']:

            def closure(name):

                strip_name = strip_prefix + name.capitalize()
                ab_strip_name = strip_prefix + 'AB' + name.capitalize()

                def getter(mute, ab_mute):
                    if mute == 0.0 and ab_mute == 0.0:
                        return 'on'
                    elif mute == 1.0 and ab_mute == 1.0:
                        return 'off'
                    else:
                        return '?'

                def setter(state):
                    if state == 'on':
                        self.set(strip_name, 'Gain', 'Mute', 0.0)
                        self.set(ab_strip_name, 'Gain', 'Mute', 0.0)
                        for vx in ['normo', 'gars', 'meuf']:
                            if vx != name:
                                vx_strip_name = strip_prefix + vx.capitalize()
                                self.set(vx_strip_name, 'Aux%20(A)', 'Gain', 0)
                                self.set(vx_strip_name, 'Aux%20(B)', 'Gain', -70)

                    elif state == 'off':
                        self.set(strip_name, 'Gain', 'Mute', 1.0)
                        self.set(ab_strip_name, 'Gain', 'Mute', 1.0)

                self.add_meta_parameter(
                    name,
                    [[strip_name, 'Gain', 'Mute'], [ab_strip_name, 'Gain', 'Mute']],
                    getter,
                    setter
                )

            closure(name)


        for name in ['normo', 'gars', 'meuf']:

            def closure(name):

                self.add_meta_parameter(
                    name + '_exclu',
                    ['normo', 'gars', 'meuf'],
                    lambda n,g,m: None,
                    lambda state: [self.set(n, 'on' if n == name else 'off') for n in ['normo', 'gars', 'meuf']]
                )

            closure(name)
