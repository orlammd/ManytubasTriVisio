from ..base import RouteBase, mk2_button, pedalboard_button
from .video import Video
from .light import Light

from modules import *

class Snapshat(Video, Light, RouteBase):

    def activate(self):
        """
        Called when the engine switches to this route.
        """

        super().activate()

        transport.set_tempo(90)
        transport.set_cycle('4/4')

        # Setups, banks...
        seq192.set_screenset(self.name)
        prodSampler.set_kit(self.name)

        # Microtonality
        microtonality.enable()
        microtonality.set_tuning(0, 0, 0, 0.35, 0, 0, 0, 0, 0, 0, 0.35, 0)

    @pedalboard_button(1)
    @mk2_button(1, 'blue')
    def stop(self):
        """
        STOP
        """
        self.pause_loopers()
        transport.stop()

    @pedalboard_button(2)
    def pont(self):
        """
        PONT / INTRO
        """
        self.pause_loopers()
        self.reset()

        # Sequences
        seq192.select('solo', 'pont_*')

        # Transport
        transport.start()

        # Samples
        samplesFX6Scape.set('Samples1', 'Gain', 'Gain', -6.0)
        samplesFX6Scape.set('SamplesFX6Scape', 'Gain', 'Mute', 0.0)
        samples.set('Samples1', 'Gain', 'Mute', 0.0)

        prodSampler.send("/instrument/stop", "s:Plagiat/Snapshat/Koto0")
        constantSampler.send("/instrument/stop", "s:BoringBloke")

        # Vocals
        vocalsNano.set('gars_exclu', 'on')
        vocalsKesch.set('meuf_exclu', 'on')

    @pedalboard_button(3)
    def couplet(self):
        """
        COUPLET
        """
        self.pause_loopers()
        self.reset()

        # Sequences
        seq192.select('solo', 'couplet_*')

        # Transport
        transport.start()

        # Samples
        samplesFX6Scape.set('Samples1', 'Gain', 'Gain', -6.0)
        samplesFX6Scape.set('SamplesFX6Scape', 'Gain', 'Mute', 0.0)
        samples.set('Samples1', 'Gain', 'Mute', 0.0)

        # Vocals
        vocalsNano.set('meuf_exclu', 'on')
        vocalsKesch.set('meuf_exclu', 'on')


    @pedalboard_button(4)
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
        samplesFX6Scape.set('Samples1', 'Gain', 'Gain', -6.0)
        samplesFX6Scape.set('SamplesFX6Scape', 'Gain', 'Mute', 0.0)
        samples.set('Samples1', 'Gain', 'Mute', 0.0)
        samples.set('Samples2', 'Gain', 'Mute', 0.0)

        # Vocals
        vocalsNano.set('meuf_exclu', 'on')
        vocalsNanoFX2Delay.set('NanoMeuf', 'Gain', 'Gain', 0.0)
        vocalsNanoFX2Delay.set('VocalsNanoFX2Delay', 'Gain', 'Mute', 0.0)
        vocalsKesch.set('gars_exclu', 'on')
        vocalsKeschFX2Delay.set('KeschMeuf', 'Gain', 'Gain', 0.0)
        vocalsKeschFX2Delay.set('VocalsKeschFX2Delay', 'Gain', 'Mute', 0.0)

        # Sequences (Mentat)
        self.start_sequence('refrain', {
            'signature': '8/4',
            1: lambda: vocalsKesch.set('gars_exclu', 'on'),
            6: lambda: vocalsKesch.set('meuf_exclu', 'on'),
        })

    @mk2_button(2, 'purple')
    def contrechant(self):
        """
        CONTRECHANT (couplet)
        """
        # Sequences
        seq192.select('on', 'contrechant_*')

        # Vocals
        vocalsNanoFX3TrapVerb.set('NanoMeuf', 'Gain', 'Gain', -70.0) # en cas de sortie de Trap
        vocalsNanoFX3TrapVerb.set('VocalsNanoFX3TrapVerb', 'Gain', 'Mute', 1.0)


    @mk2_button(3, 'purple')
    def trap(self):
        """
        TRAP (couplet)
        """
        # Vocals
        vocalsNanoFX3TrapVerb.set('NanoMeuf', 'Gain', 'Gain', 0.0)
        vocalsNanoFX3TrapVerb.set('VocalsNanoFX3TrapVerb', 'Gain', 'Mute', 0.0)

        # Samples
        postprocess.animate_filter('Samples', 20000, 1000, 1)

        # Keyboards
        jmjKeyboard.set_sound('LowCTrap1')

    @pedalboard_button(11)
    def goto_mcob(self):
        """
        GOTO MCOB
        """
        engine.set_route('Mcob')
        engine.active_route.intro()

    @mk2_button(6, 'yellow')
    def nanomeuf(self):
        """
        VOCALS NANO ++
        """
        vocalsNano.set('meuf_exclu', 'on')

    @mk2_button(7, 'yellow')
    def nanonormo(self):
        """
        VOCALS NANO ==
        """
        vocalsNano.set('normo_exclu', 'on')

    @mk2_button(8, 'yellow')
    def nanogars(self):
        """
        VOCALS NANO --
        """
        vocalsNano.set('gars_exclu', 'on')
