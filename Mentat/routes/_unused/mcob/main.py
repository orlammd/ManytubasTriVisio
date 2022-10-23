from ..base import RouteBase, mk2_button, pedalboard_button
from .video import Video
from .light import Light

from modules import *

class Mcob(Video, Light, RouteBase):
    """
    MCOB
    """

    def activate(self):
        """
        Called when the engine switches to this route.
        """

        super().activate()

        transport.set_tempo(120)
        transport.set_cycle('4/4')

        # Setups, banks...
        seq192.set_screenset(self.name)
        prodSampler.set_kit(self.name)

        # Microtonality
        microtonality.enable()
        microtonality.set_tuning(0, 0, 0, 0, 0, 0.35, 0, 0, 0.35, 0, 0.35, 0)


    @pedalboard_button(1)
    @mk2_button(1, 'blue')
    def stop(self):
        """
        STOP
        zazad
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
        transport.set_tempo(120)
        transport.start()

        # Samples
        samplesFX6Scape.set('Samples2', 'Gain', 'Gain', -5.0)
        samplesFX6Scape.set('SamplesFX6Scape', 'Gain', 'Mute', 0.0)

        samples.set('Samples1', 'Gain', 'Mute', 0.0)
        samples.set('Samples2', 'Gain', 'Mute', 0.0)
        samples.set('Samples5', 'Gain', 'Mute', 0.0)

        # Vocals
        vocalsNano.set('gars_exclu', 'on')
        vocalsKesch.set('meuf_exclu', 'on')

        # Keyboard
        jmjKeyboard.set_sound('LowZDupieux')

    @pedalboard_button(5)
    def prerefrain0(self):
        """
        PRÉ-REFRAIN 0 (cf PRÉ-REFRAIN)
        """
        # méthode vide juste pour que le déroulé du morceau appairaisse de façon linéaire
        pass



    @mk2_button(2, 'purple')
    def refrain(self):
        """
        REFRAIN
        """
        self.pause_loopers()
        self.reset()

        # Sequences
        seq192.select('solo', 'refrain_*')

        # Transport
        transport.set_tempo(120)
        transport.start()

        # Samples
        samplesFX6Scape.set('Samples2', 'Gain', 'Gain', -5.0)
        samplesFX6Scape.set('SamplesFX6Scape', 'Gain', 'Mute', 0.0)

        samples.set('Samples1', 'Gain', 'Mute', 0.0)
        samples.set('Samples2', 'Gain', 'Mute', 0.0)
        samples.set('Samples3', 'Gain', 'Mute', 0.0)
        samples.set('Samples5', 'Gain', 'Mute', 0.0)

        # Bass
        bassfx.set('distohi', 'on')

        # Vocals
        vocalsNano.set('meuf_exclu', 'on')
        vocalsKesch.set('meuf_exclu', 'on')

        # Keyboards
        jmjKeyboard.set_sound('LowZDubstep')

    @pedalboard_button(3)
    def couplet1_1(self):
        """
        COUPLET 1 - Trap "Look"
        """
        self.pause_loopers()
        self.reset()

        # Sequences
        seq192.select('solo', 'couplet1-1_*')

        # Transport
        transport.set_tempo(120)
        transport.start()

        # Samples
        samplesFX6Scape.set('Samples2', 'Gain', 'Gain', -10.0) # attention - 10 et - 5 dans setup précédent
        samplesFX6Scape.set('SamplesFX6Scape', 'Gain', 'Mute', 0.0)

        samplesFX2Delay.set('Samples2', 'Gain', 'Gain', -9.0)
        samplesFX2Delay.set('SamplesFX2Delay', 'Gain', 'Mute', 0.0)

        samples.set('Samples1', 'Gain', 'Mute', 0.0)
        samples.set('Samples2', 'Gain', 'Mute', 0.0)
        samples.set('Samples4', 'Gain', 'Mute', 0.0)


        # Vocals
        vocalsNano.set('meuf_exclu', 'on')
        vocalsKesch.set('gars_exclu', 'on')

        vocalsNanoFX3TrapVerb.set('NanoMeuf', 'Gain', 'Gain', 0.0)
        vocalsNanoFX3TrapVerb.set('VocalsNanoFX3TrapVerb', 'Gain', 'Mute', 0.0)

    @pedalboard_button(4)
    def couplet1_2(self):
        """
        COUPLET 1 - Prince 2 Pac
        """
        # Sequences
        seq192.select('solo', 'couplet1-2_*')
        seq192.select('off', 'couplet1-2_samples_princeguitar2')

        # Samples
        samplesFX6Scape.set('Samples2', 'Gain', 'Gain', -10.0) # attention - 10 et - 5 dans setup précédent
        samplesFX6Scape.set('SamplesFX6Scape', 'Gain', 'Mute', 0.0)

        samplesFX2Delay.set('Samples2', 'Gain', 'Gain', -9.0)
        samplesFX2Delay.set('SamplesFX2Delay', 'Gain', 'Mute', 0.0)

        samples.set('Samples1', 'Gain', 'Mute', 0.0)
        samples.set('Samples2', 'Gain', 'Mute', 0.0)
        samples.set('Samples4', 'Gain', 'Mute', 0.0)

        # Vocals
        vocalsNano.set('meuf_exclu', 'on')
        vocalsKesch.set('gars_exclu', 'on')

        # Sequences (Mentat)
        self.start_scene('prince2pac_launcher', lambda: [
            self.wait_next_cycle(),
            self.start_sequence('prince2pac_a', [
                {   # bar 1
                    'signature': '4/4',
                    1: lambda: vocalsKesch.set('gars_exclu', 'on')
                },
                {}, {}, {}, {}, {}, # bars 2, 3, 4, 5, 6,
                {   # bar 7
                    1: lambda: [vocalsKesch.set('gars', 'on'), vocalsKesch.set('normo', 'on')]
                },
                {}, {}, # bars 8, 9
                {   # bar 10
                    1: lambda: vocalsKesch.set('normo_exclu', 'on')
                },
                {}, {}, # bars 11, 12
                {   # bar 13
                    2: lambda: vocalsKesch.set('meuf', 'on'),
                    3: lambda: vocalsKesch.set('meuf', 'off'),
                    4: lambda: vocalsKesch.set('meuf', 'on'),
                },
                {   # bar 14
                    1: lambda: vocalsKesch.set('meuf', 'off'),
                },
                {}, # bar 15
                {   # bar 16
                    4: lambda: postprocess.animate_pitch('*', 1, 0.25, 0.5, 'beat'),
                    4.95: lambda: postprocess.animate_pitch('*', 0.25, 1, 0.05, 'beat')
                },
                {  # bar 17
                    1: lambda: [seq192.select('off', 'couplet1-2_cLow_*'), seq192.select('off', 'couplet1-2_samples_princeguitar'), seq192.select('on', 'couplet1-2_samples_princeguitar2'), seq192.select('on', 'couplet1-2_cLow_trap1')]
                    # On coupe le bass synth et allez hop bass/batt
                },
            ], loop=False),
        ])

    @mk2_button(3, 'purple')
    def couplet1_3(self):
        """
        COUPLET 1 - Shaft
        """
        # Sequences
        seq192.select('solo', 'couplet1-2_*')
        seq192.select('off', 'couplet1-2_samples_princeguitar2')
        seq192.select('off', 'couplet1-2_cLow_*')

        # Transport
        transport.set_tempo(120)
        transport.start()

        # Vocals
        vocalsNano.set('gars', 'on')
        vocalsNano.set('normo', 'on')
        vocalsKesch.set('gars_exclu', 'on')

        # Sequences (Mentat)
        self.start_sequence('prince2pac_b', [
            {   # bar 1
                'signature': '4/4',
                1: lambda: [vocalsKesch.set('meuf_exclu', 'on'), vocalsKesch.set('normo', 'on')],
            },
            {  # bar 2
                3 + 2/3: lambda: vocalsKesch.set('gars_exclu', 'on'),
            },
            {  # bar 3
                1: lambda: seq192.select('on', 'couplet1-2_cLow_*')
            }, {}, # bar 4
            {   # bar 5
                1: lambda: vocalsKesch.set('gars_exclu', 'on')
            },
            {}, {}, # bar 6, 7
            {   # bar 8
                4 + 2/3: lambda: vocalsKesch.set('normo', 'on')
            },
            {}, {}, # bar 9, 10
            {   # bar 11
                1: lambda: vocalsKesch.set('normo_exclu', 'on'),
                3: lambda: vocalsKesch.set('meuf', 'on')
            },
            {   # bar 12
                1: lambda: vocalsKesch.set('meuf', 'off'),
                4.5: lambda: vocalsKesch.set('meuf', 'on')
            },
            {   # bar 13
                2.5: lambda: vocalsKesch.set('meuf', 'off'),
                3: lambda: vocalsKesch.set('meuf', 'on'),
                4.5: lambda: vocalsKesch.set('meuf', 'off'),
            },
            {   # bar 14
                1: lambda: vocalsKesch.set('meuf', 'on'),
            },
            {   # bar 15
                2.5: lambda: vocalsKesch.set('meuf', 'off'),
                3: lambda: vocalsKesch.set('meuf', 'on')
            },
            {}, {},  # bar 16, 17
        ], loop=False)


    @mk2_button(4, 'purple')
    def couplet1_4(self):
        """
        COUPLET 1 - Ragga
        """
        self.pause_loopers()
        self.reset()

        # Sequences
        seq192.select('solo', 'couplet1-4_*')

        # Transport
        transport.set_tempo(120)
        transport.start()

        # Samples
        samplesFX6Scape.set('Samples2', 'Gain', 'Gain', -10.0) # attention - 10 et - 5 dans setup précédent
        samplesFX6Scape.set('SamplesFX6Scape', 'Gain', 'Mute', 0.0)

        samplesFX2Delay.set('Samples2', 'Gain', 'Gain', -9.0)
        samplesFX2Delay.set('SamplesFX2Delay', 'Gain', 'Mute', 0.0)

        samples.set('Samples1', 'Gain', 'Mute', 0.0)
        samples.set('Samples2', 'Gain', 'Mute', 0.0)
        samples.set('Samples4', 'Gain', 'Mute', 0.0)

        # Vocals
        vocalsKesch.set('meuf_exclu', 'on')
        vocalsNano.set('gars_exclu', 'on')

    @pedalboard_button(5)
    def prerefrain(self):
        """
        PRE-REFRAIN
        """
        self.pause_loopers()
        self.reset()

        # Sequences
        seq192.select('solo', 'prerefrain_*')

        # Transport
        transport.set_tempo(120)
        transport.start()

        # Samples
        samplesFX6Scape.set('Samples2', 'Gain', 'Gain', -5.0)
        samplesFX6Scape.set('SamplesFX6Scape', 'Gain', 'Mute', 0.0)

        samples.set('Samples1', 'Gain', 'Mute', 0.0)
        samples.set('Samples2', 'Gain', 'Mute', 0.0)
        samples.set('Samples5', 'Gain', 'Mute', 0.0)

        # Vocals
        vocalsKesch.set('gars', 'on')
        vocalsKesch.set('meuf', 'on')
        vocalsNano.set('normo_exclu', 'on')

        # Keyboards
        jmjKeyboard.set_sound('ConstantSampler')

    @mk2_button(2)
    def refrain2(self):
        """
        REFRAIN 2 (cf REFRAIN)
        """
        # méthode vide juste pour que le déroulé du morceau appairaisse de façon linéaire
        pass

    @pedalboard_button(6)
    def couplet2(self):
        """
        COUPLET 2
        """
        self.pause_loopers()
        self.reset()

        # Looper
        looper.record_on_start(0)

        # Sequences
        seq192.select('solo', 'couplet2_*')

        # Transport
        transport.set_tempo(120)
        transport.start()

        # Samples
        samplesFX6Scape.set('Samples2', 'Gain', 'Gain', -10.0) # attention - 10 et - 5 dans setup précédent
        samplesFX6Scape.set('SamplesFX6Scape', 'Gain', 'Mute', 0.0)

        samplesFX2Delay.set('Samples2', 'Gain', 'Gain', -9.0)
        samplesFX2Delay.set('SamplesFX2Delay', 'Gain', 'Mute', 0.0)

        samples.set('Samples1', 'Gain', 'Mute', 0.0)
        samples.set('Samples2', 'Gain', 'Mute', 0.0)
        samples.set('Samples4', 'Gain', 'Mute', 0.0)

        # Vocals
        vocalsKesch.set('gars', 'on')
        vocalsKesch.set('meuf', 'on')
        vocalsNano.set('normo_exclu', 'on')

        # Keyboards
        jmjKeyboard.set_sound('ZNotSoRhodes')

    @mk2_button(4)
    def couplet2_1(self):
        """
        Couplet 2-1 (RAGGA) (cf Couplet 1-4)
        """
        # méthode vide juste pour que le déroulé du morceau appairaisse de façon linéaire
        pass

    @pedalboard_button(7)
    def blast(self):
        """
        BLAST
        """
        self.pause_loopers()
        self.reset()

        # Sequences
        seq192.select('solo', 'blast1_*')

        # Transport
        transport.start()
        transport.set_tempo(120)

        # Samples
        samplesFX6Scape.set('Samples2', 'Gain', 'Gain', -5.0)
        samplesFX6Scape.set('SamplesFX6Scape', 'Gain', 'Mute', 0.0)

        samples.set('Samples1', 'Gain', 'Mute', 0.0)
        samples.set('Samples2', 'Gain', 'Mute', 0.0)
        samples.set('Samples3', 'Gain', 'Mute', 0.0)
        samples.set('Samples5', 'Gain', 'Mute', 0.0)

        # Scenes
        self.start_sequence('delayed_blast', {
            'signature': '32/4',
            33: lambda: seq192.select('solo', 'blast2_*'),
        })


    @pedalboard_button(8)
    def trance(self):
        """
        TRANCE
        """
        self.pause_loopers()
        self.reset()

        # Sequences
        seq192.select('solo', 'trance_*')

        # Samples
        samplesFX6Scape.set('Samples2', 'Gain', 'Gain', -5.0)
        samplesFX6Scape.set('SamplesFX6Scape', 'Gain', 'Mute', 0.0)

        samples.set('Samples1', 'Gain', 'Mute', 0.0)
        samples.set('Samples2', 'Gain', 'Mute', 0.0)
        samples.set('Samples5', 'Gain', 'Mute', 0.0)

        # Transport
        transport.start()
        transport.set_tempo(130)

    @pedalboard_button(9)
    def rec_synth(self):
        """
        RECORD SYNTH
        """
        looper.record(7)

    @pedalboard_button(10)
    def loop_synth(self):
        """
        OVERDUB SYNTH
        """
        looper.overdub(7)

    @mk2_button(5, 'purple')
    def relance_trance(self):
        """
        RELANCE TRANCE
        """
        self.pause_loopers()
        self.reset()

        seq192.select('off', '*')

        # Looper
        looper.trigger('[0,3,7]')

        # Transport
        transport.set_tempo(130)
        transport.start()

        # Samples
        samplesFX6Scape.set('Samples2', 'Gain', 'Gain', -5.0)
        samplesFX6Scape.set('SamplesFX6Scape', 'Gain', 'Mute', 0.0)

        samples.set('Samples1', 'Gain', 'Mute', 0.0)
        samples.set('Samples2', 'Gain', 'Mute', 0.0)
        samples.set('Samples5', 'Gain', 'Mute', 0.0)

        # Vocals
        vocalsKesch.set('meuf_exclu', 'on') # TODO delay
        vocalsNano.set('meuf_exclu', 'on')
