from ..base import RouteBase, mk2_button, pedalboard_button
from .video import Video
from .light import Light

from modules import *

class SaperComJaja(Video, Light, RouteBase):

    def activate(self):
        """
        Called when the engine switches to this route.
        """

        super().activate()

        # Transport
        transport.set_tempo(150)
        transport.set_cycle('3/4', pattern="Xxx")

        # Setups, banks...
        seq192.set_screenset(self.name)
        prodSampler.set_kit('AgneauGastrik')

        # Microtonality
        microtonality.enable()
        microtonality.set_tuning(0, 0, 0, 0, 0, 0.35, 0, 0, 0.35, 0, 0.35, 0)

    def couplet_m(self):
        """
        Couplets M
        """
        self.pause_loopers()
        self.reset()

        # Sequences
        seq192.select('solo', 'couplet_m_*')

        # Transport
        transport.set_cycle('3/4', pattern="Xxx")
        transport.start()

        # Samples
        samples.set('Samples4', 'Gain', 'Mute', 0.0)

        # Keyboards
        jmjKeyboard.set_sound('CLowBoomTrapLine')
        #### TODO mk2Keyboard ?

    @pedalboard_button(1)
    @mk2_button(1, 'blue')
    def stop(self):
        """
        STOP
        """
        self.pause_loopers()
        transport.stop()

    @pedalboard_button(2) # bouton 5 à l'origine
    def ethiotrap(self):
        """
        EthioTrap
        """
        self.pause_loopers()
        self.reset()

        # Sequences
        seq192.select('solo', 'ethiotrap_*')

        # Transport
        transport.start()

        # Samples
        samples.set('Samples4', 'Gain', 'Mute', 0.0)

        # Vocals
        vocalsNano.set('gars_exclu', 'on')
        vocalsKesch.set('normo_exclu', 'on')

        # Keyboards
        jmjKeyboard.set_sound('CTrap')
        #### TODO mk2Keyboard ?

    @pedalboard_button(3) # bouton 6 à l'origine
    def mandelaaa(self):
        """
        Mandela A A A
        """
        self.pause_loopers()
        self.reset()

        # Sequences
        seq192.select('solo', 'mandelaaa_*')

        # Transport
        transport.set_cycle('4/4', pattern="Xxxx")
        transport.start()

        # Samples
        samples.set('Samples4', 'Gain', 'Mute', 0.0)

        # Vocals
        vocalsNano.set('normo_exclu', 'on')
        vocalsKesch.set('meuf_exclu', 'on')

        # Keyboards
        jmjKeyboard.set_sound('LowCTrap1')

    @pedalboard_button(4) # bouton 7 à l'origine
    def couplet_m1(self):
        """
        Couplet M 1
        """
        self.couplet_m()

        # Vocals
        vocalsNano.set('gars_exclu', 'on')
        vocalsKesch.set('normo_exclu', 'on')

    @mk2_button(2, 'purple') # à l'origine bouton 6
    def zynette_dre(self):
        """
        Zynette Dre
        """
        
        self.couplet_m1()

        # Sequences
        seq192.select('on', 'zynette_*')


    @pedalboard_button(3) # bouton 6 à l'origine
    def mandelaaa2(self):
        """
        Mandela A A A (cf. mandelaaa)
        """
        # méthode vide juste pour que le déroulé du morceau appairaisse de façon linéaire
        pass

    @pedalboard_button(5) # bouton 8 à l'origine
    def couplet_m2(self):
        """
        Couplet M 2
        """
        self.couplet_m()

        # Vocals
        vocalsNano.set('gars_exclu', 'on')
        vocalsKesch.set('meuf_exclu', 'on')

    @mk2_button(2, 'purple') # à l'origine bouton 6
    def zynette_dre2(self):
        """
        Zynette Dre (cf. zynette_dre)
        """
        # méthode vide juste pour que le déroulé du morceau appairaisse de façon linéaire
        pass

    @pedalboard_button(6) # bouton 9 à l'origine
    def eggz_trapcut(self):
        """
        Mamaz Bakingz Eggz
        """
        #### TODO scène trapcut

    @pedalboard_button(7) # bouton 10 à l'origine
    def rimdogged(self):
        """
        RimDoooooooooged
        """

        # Transport
        transport.stop()

        # Vocals
        vocalsNano.set('normo_exclu', 'on')
        vocalsNanoFX4Disint.set('NanoNormo', 'Gain', 'Mute', 0.0)

        # Keyboards
        jmjKeyboard.set_sound('CDubstepHorn')

    @pedalboard_button(8) # bouton 11 à l'origine
    def mandelaaa_final(self):
        """
        Mandela A A A A Final
        """

        # Sequences
        seq192.select('solo', 'mandelaaa_*')
        seq192.select('on', 'mandelaaafinal_*')

        # Transport
        transport.set_cycle('4/4', pattern="Xxxx")
        transport.start()

        # Samples
        samples.set('Samples4', 'Gain', 'Mute', 0.0)

        # Vocals
        vocalsNano.set('normo_exclu', 'on')
        vocalsKesch.set('meuf_exclu', 'on')

        # Keyboards
        jmjKeyboard.set_sound('CDubstepHorn')

    #### TODO Méthodes boutons 7 & 8 Jeannot Cock your butter gun?
