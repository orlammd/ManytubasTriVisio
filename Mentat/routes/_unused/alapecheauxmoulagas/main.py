from ..base import RouteBase, mk2_button, pedalboard_button
from .video import Video
from .light import Light

from modules import *

class Alapecheauxmoulagas(Video, Light, RouteBase):
    """
    A la pêche aux Moulagas
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
        microtonality.set_tuning(0, 0, 0, 0.35, 0, 0, 0, 0, 0, 0, 0.35, 0)


    @pedalboard_button(1)
    @mk2_button(1, 'blue')
    def stop(self):
        """
        STOP
        zazad
        """
        self.pause_loopers()
        transport.stop()

    mk2_button(6)
    def bipbip(self):
        pass

    mk2_button(7)
    def notappropriate(self):
        pass

    mk2_button(8)
    def alahialaha(self):
        pass

    @mk2_button(2)
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

        # Vocals
        vocalsNano.set('gars_exclu', 'on')
        vocalsKesch.set('gars_exclu', 'on')


    """
    REFRAIN / THÊME
    """

    """
    COUPLET NANO
    """

    """
    COUPLET KESCH
    """
