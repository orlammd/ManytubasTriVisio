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
                        samples.set('Samples1', 'Gain', 'Mute', 0.0),
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
