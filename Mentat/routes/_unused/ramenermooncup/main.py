from ..base import RouteBase, mk2_button, pedalboard_button
from .video import Video
from .light import Light

from modules import *

class RamenerMooncup(Video, Light, RouteBase):

    def activate(self):
        """
        Called when the engine switches to this route.
        """

        super().activate()

        transport.set_tempo(150)
        transport.set_cycle('4/4')

        # Setups, banks...
        seq192.set_screenset(self.name)
        prodSampler.set_kit(self.name)

        # Microtonality
        microtonality.enable()
        microtonality.set_tuning(0, 0, 0, 0, 0, 0.35, 0, 0, -0.35, 0, 0.35, 0)

    @pedalboard_button(1)
    @mk2_button(1, 'blue')
    def stop(self):
        """
        STOP
        """
        self.pause_loopers()
        transport.stop()

    @pedalboard_button(2)
    def intro(self):
        """
        INTRO
        """
        self.pause_loopers()
        self.reset()

        # Sequences
        seq192.select('solo', 'intro_*')

        # Transport
        transport.start()

        # Samples
        samples.set('Samples1', 'Gain', 'Mute', 0.0)
        samples.set('Samples2', 'Gain', 'Mute', 0.0)
        samples.set('Samples3', 'Gain', 'Mute', 0.0)
        samples.set('Samples4', 'Gain', 'Mute', 0.0)
        samples.set('Samples5', 'Gain', 'Mute', 0.0)

        # Vocals
        vocalsNano.set('gars_exclu', 'on')
        vocalsKesch.set('meuf_exclu', 'on')

    @mk2_button(2, 'purple')
    def couplet1(self):
        """
        COUPLET 1
        """
        # Samples
        samples.set('Samples1', 'Gain', 'Mute', 0.0)
        samples.set('Samples[1-5]', 'Gain', 'Gain', -9.0)
        samplesFX2Delay.set('Samples[1-5]', 'Gain', 'Gain', -9.0)
        samplesFX2Delay.set('SamplesFX2Delay', 'Gain', 'Mute', 0.0)
        postprocess.animate_pitch('*', 1, 0.25, 0.75)

        # TODO ???: envoyer samples dans la reverb
        # TODO ???: stereo samples

        # Looper
        looper.record(0)

        # Sequences (Mentat)
        self.start_scene('sequence/couplet1_delayed', lambda:[
            self.wait_next_cycle(),
            postprocess.animate_pitch('*', None, 1, 0.1),

            self.start_sequence('couplet', [
                *[{} for i in range(7)], # bars 1 - 7
                { # bar 8
                    4: lambda: looper.record(0)
                },
                *[{} for i in range(29)], # bars 9 - 21
                { # bar 22
                    1: lambda: postprocess.animate_pitch(['Samples*', 'Synths*'], 1, 0.25, 1),
                    2: lambda: seq192.select('solo', 'dummy'),
                    2 + 0.4: lambda: postprocess.animate_pitch(['Samples*', 'Synths*'], None, 1, 0.1),
                    2 + 1/2. : lambda: [
                        samples.set('Samples[1-5]', 'Gain', 'Gain', 0.0),
                        samplesFX1Delay.set('Samples[1-5]', 'Gain', 'Gain', 0.0),
                        samplesFX6Scape.set('Samples[1-5]', 'Gain', 'Gain', 0.0),
                        samplesFX5TapeDelay.set('Samples[1-5]', 'Gain', 'Gain', 0.0),
                        samplesFX1Delay.set('SamplesFX1Delay', 'Gain', 'Mute', 0.0),
                        samplesFX6Scape.set('SamplesFX6Scape', 'Gain', 'Mute', 0.0),
                        samplesFX5TapeDelay.set('SamplesFX5TapeDelay', 'Gain', 'Gain', 0.0),

                        # Sequences
                        seq192.select('solo', 'couplet1_*'),
                        seq192.select('on', 'intro_samples_voix4'),

                        # Vocals
                        vocalsNano.set('meuf_exclu', 'on'),
                        vocalsKesch.set('gars_exclu', 'on')
                    ],
                },
            ], loop=False)


        ])

    @mk2_button(3, 'purple')
    def refrain(self):
        """
        REFRAIN
        """
        self.pause_loopers()
        self.reset()

        # Sequences
        seq192.select('solo', 'refrain_*')

        # Transport
        transport.start()

        # Samples
        samples.set('Samples1', 'Gain', 'Mute', 0.0)
        samplesFX1Delay.set('Samples1', 'Gain', 'Gain', 0.0),
        samplesFX6Scape.set('Samples1', 'Gain', 'Gain', 0.0),
        samplesFX5TapeDelay.set('Samples1', 'Gain', 'Gain', 0.0),
        samplesFX1Delay.set('SamplesFX1Delay', 'Gain', 'Mute', 0.0),
        samplesFX6Scape.set('SamplesFX6Scape', 'Gain', 'Mute', 0.0),
        samplesFX5TapeDelay.set('SamplesFX5TapeDelay', 'Gain', 'Gain', 0.0),


        # Vocals
        vocalsNano.set('normo_exclu', 'on')
        vocalsKesch.set('gars_exclu', 'on')

    @mk2_button(4, 'purple')
    def couplet2_intro(self):
        """
        COUPLET 2 (INTRO)
        """
        self.pause_loopers()
        self.reset()

        # Sequences
        seq192.select('solo', 'couplet2-1_*')

        # Transport
        transport.start()

        # Samples
        samples.set('Samples[1-5]', 'Gain', 'Mute', 0.0)

        # Keyboards
        jmjKeyboard.set_sound('LowZDancestep')

        # Vocals
        vocalsNano.set('gars_exclu', 'on')
        vocalsKesch.set('normo_exclu', 'on')
        vocalsKesch.set('meuf', 'on')

    @pedalboard_button(4)
    def couplet2_main(self):
        """
        COUPLET 2 (MAIN - "Should I...")
        """
        self.pause_loopers()
        self.reset()

        # Sequences
        seq192.select('solo', 'couplet2-2_*')

        # Transport
        transport.start()

        # Samples
        samples.set('Samples1', 'Gain', 'Mute', 0.0)
        samplesFX1Delay.set('Samples1', 'Gain', 'Gain', 0.0),
        samplesFX6Scape.set('Samples1', 'Gain', 'Gain', 0.0),
        samplesFX5TapeDelay.set('Samples1', 'Gain', 'Gain', 0.0),
        samplesFX1Delay.set('SamplesFX1Delay', 'Gain', 'Mute', 0.0),
        samplesFX6Scape.set('SamplesFX6Scape', 'Gain', 'Mute', 0.0),
        samplesFX5TapeDelay.set('SamplesFX5TapeDelay', 'Gain', 'Gain', 0.0),


        # Keyboards
        jmjKeyboard.set_sound('LowZDancestep')

        # Vocals
        vocalsNano.set('meuf_exclu', 'on')
        vocalsKesch.set('gars_exclu', 'on')

    self.start_sequence('couplet2-2', [
        *[{} for i in range(15)], # bars 1 - 15
        { # bar 16
            3 + 1/2.: lambda: [

                # Looper
                looper.trig(0),

                # Vocals
                vocalsKesch.set('meuf_exclu', 'on')
            ]
        },
        { # bar 17
            1: lambda: [
                # Samples
                samples.set('Samples[1-5]', 'Gain', 'Mute', 0.0),

                # Sequences
                seq192.set('on', 'couplet2-3'),

                # Vocals
                vocalsNano.set('gars_exclu', 'on')
            ]
        }
    ], loop=False)

    @mk2_button(3, 'purple')
    def refrain2(self):
        """
        REFRAIN (cf. REFRAIN)
        """
        pass

    @pedalboard_button(5)
    def refrain_messe(self):
        """
        REFRAIN MESSE
        """
        self.pause_loopers()
        self.reset()

        # Transport
        transport.stop()

        # Keyboards
        jmjKeyboard.set_sound('ZOrgan')

        # Vocals
        vocalsNano.set('normo_exclu', 'on')
        vocalsKesch.set('normo_exclu', 'on')

    @pedalboard_button(6)
    @pedalboard_button(7)
    def disco(self):
        """
        DISCO (6) / DROP THE BASS (7)
        """
        self.pause_loopers()
        self.reset()

        # Sequences
        seq192.select('solo', 'disco_*')

        # Transport
        transport.start()

        # Samples
        samples.set('Samples1', 'Gain', 'Mute', 0.0)

        # Keyboards
        jmjKeyboard.set_sound('LowZDubstep')

        # Vocals
        vocalsNano.set('gars_exclu', 'on')
        vocalsKesch.set('gars_exclu', 'on')

    @pedalboard_button(8)
    def ramener_launcher(self):
        """
        RAMENER LAUNCHER
        """
        self.pause_loopers()
        self.reset()

        # Sequences
        seq192.select('solo', 'ramener0_*')

        # Transport
        transport.start()

        # Samples
        samples.set('Samples1', 'Gain', 'Mute', 0.0)

        # Keyboards
        jmjKeyboard.set_sound('LowZDancestep')

        # Vocals
        vocalsNano.set('gars_exclu', 'on')
        vocalsKesch.set('gars_exclu', 'on')

        self.start_sequence('ramener', [
            {}, {}, # bars 1-2
            {
                3: lambda: postprocess.animate_pitch('Samples', 1, 0.25, 2),
                4 + 1/2.: seq192.select('solo', 'dummy')
            },
            {
                seq192.select('solo', 'ramener*') #### TODO : vérifier qu'il y a bien ça ???
            }
        ], loop=False)


    @pedalboard_button(9)
    def ramener_mesh(self):
        """
        RAMENER MESSHUGAH
        """
        self.pause_loopers()
        self.reset()

        # Sequences
        seq192.select('solo', 'ramener0_*')

        # Transport
        transport.stop()

        # Samples
        samples.set('Samples1', 'Gain', 'Mute', 0.0)
        #### TODO constantSampler.send('/instrument/play', 's:Plagiat/RamenerMooncup/') #### METTRE LE SAMPLE DANS CONSTANTSAMPLER

        # Vocals
        vocalsNano.set('meuf_exclu', 'on')
        vocalsNano.set('normo', 'on')
        vocalsNano.set('gars', 'on')
        vocalsNanoFX2Delay.set('Nano*', 'Gain', 'Gain', 0.0)
        vocalsNanoFX2Delay.set('VocalsNanoFX2Delay', 'Gain', 'Mute', 0.0)
        vocalsKesch.set('meuf_exclu', 'on')
        vocalsKesch.set('normo', 'on')
        vocalsKesch.set('gars', 'on')
        vocalsKeschFX2Delay.set('Kesch*', 'Gain', 'Gain', 0.0)
        vocalsKeschFX2Delay.set('VocalsKeschFX2Delay', 'Gain', 'Mute', 0.0)


        self.start_sequence('ramener', [
            {
                3: lambda: postprocess.animate_pitch('Samples', 1, 0.25, 2),
                4 + 1/2.: seq192.select('solo', 'dummy')
            },
            {
                # Sequences
                seq192.select('solo', 'ramener*'),

                # Transport
                transport.start(),

                # Samples
                samples.set('Samples1', 'Gain', 'Mute', 0.0)
            }
        ], loop=False)

    @pedalboard_button(10)
    def ramener(self):
        """
        RAMENER
        """
        self.pause_loopers()
        self.reset()

        # Sequences
        seq192.select('solo', 'ramener*')

        # Transport
        transport.start()

        # Samples
        samples.set('Samples1', 'Gain', 'Mute', 0.0)


        # Vocals
        vocalsNano.set('gars_exclu', 'on')
        vocalsKesch.set('gars_exclu', 'on')

    @mk2_button(6, 'yellow')
    def nanogars(self):
        """
        VOCALS NANO GARS
        """
        vocalsNano.set('gars_exclu', 'on')

    @mk2_button(7, 'yellow')
    def nanomeuf(self):
        """
        VOCALS NANO MEUF
        """
        vocalsNano.set('meuf_exclu', 'on')

    @mk2_button(6, 'yellow')
    def nanonormo(self):
        """
        VOCALS NANO NORMO
        """
        vocalsNano.set('normo_exclu', 'on')
