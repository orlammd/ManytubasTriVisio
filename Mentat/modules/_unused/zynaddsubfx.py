from mentat import Module

class ZynAddSubFx(Module):
    """
    ZynAddSubFx synthesizer
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.add_parameter('microtonality', '/microtonal/Penabled', '*', default=False)
        self.add_parameter('tuning', '/microtonal/tuning', 's', default="\n".join([str(100.0 + i * 100) for i in range(12)]).replace('1200.0', '2/1'))

    def route(self, address, args):

        if address != '/active_keys':
            for name in self.submodules:
                self.submodules[name].route(address, args)

        return False

class ZynPart(Module):
    """
    ZynAddSubFx sound, can be associated with multiple parts in zyn.
    """

    def __init__(self, *args, parts=[], **kwargs):

        super().__init__(*args, **kwargs)

        self.parts = parts
        self.feedback_addresses = {}

        for part in self.parts:
            for param in ZynPart.parameters:
                address = '/part%i%s' % (part, param)
                self.feedback_addresses[address] = [part, param]
                self.send(address)
                self.logger.debug('probe %s' % address)

    def route(self, address, args):
        """
        Store initial values of parameters
        """
        if address in self.feedback_addresses:
            part, param = self.feedback_addresses[address]
            data = ZynPart.parameters[param]
            name = '/'.join(param.split('/')[4:])
            self.add_parameter('%i/%s' % (part, name), address, data['type'], default=args[0])
            self.logger.debug('add param %s' % ['%i/%s' % (part, name), data['type'], args[0]])
            del self.feedback_addresses[address]

    def set_all(self, name, value):

        for part in self.parts:
            self.set('%i/%s' % (part, name), value)

    parameters = {
        '/kit0/adpars/GlobalPar/Reson/PmaxdB': {'type': 'i'},
        '/kit0/adpars/GlobalPar/Reson/Pcenterfreq': {'type': 'i'},
        '/kit0/adpars/GlobalPar/Reson/Poctavesfreq': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FreqLfo/Pfreq': {'type': 'f'},
        '/kit0/adpars/GlobalPar/FreqLfo/Pintensity': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FreqLfo/Pstartphase': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FreqLfo/PLFOtype': {'type': 'i', 'choices': {'sine': 0, 'triangle': 1, 'square': 2, 'ramp-up': 3, 'ramp-down': 4, 'exponential-down1': 5, 'exponential-down2': 6}},
        '/kit0/adpars/GlobalPar/FreqLfo/Prandomness': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FreqLfo/Pfreqrand': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FreqLfo/Pdelay': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FreqLfo/Pstretch': {'type': 'i'},
        '/kit0/adpars/GlobalPar/AmpLfo/Pfreq': {'type': 'f'},
        '/kit0/adpars/GlobalPar/AmpLfo/Pintensity': {'type': 'i'},
        '/kit0/adpars/GlobalPar/AmpLfo/Pstartphase': {'type': 'i'},
        '/kit0/adpars/GlobalPar/AmpLfo/PLFOtype': {'type': 'i',  'choices': {'sine': 0, 'triangle': 1, 'square': 2, 'ramp-up': 3, 'ramp-down': 4, 'exponential-down1': 5, 'exponential-down2': 6}},
        '/kit0/adpars/GlobalPar/AmpLfo/Prandomness': {'type': 'i'},
        '/kit0/adpars/GlobalPar/AmpLfo/Pfreqrand': {'type': 'i'},
        '/kit0/adpars/GlobalPar/AmpLfo/Pdelay': {'type': 'i'},
        '/kit0/adpars/GlobalPar/AmpLfo/Pstretch': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FilterLfo/Pfreq': {'type': 'f'},
        '/kit0/adpars/GlobalPar/FilterLfo/Pintensity': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FilterLfo/Pstartphase': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FilterLfo/PLFOtype': {'type': 'i',  'choices': {'sine': 0, 'triangle': 1, 'square': 2, 'ramp-up': 3, 'ramp-down': 4, 'exponential-down1': 5, 'exponential-down2': 6}},
        '/kit0/adpars/GlobalPar/FilterLfo/Prandomness': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FilterLfo/Pfreqrand': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FilterLfo/Pdelay': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FilterLfo/Pstretch': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FreqEnvelope/Penvpoints': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FreqEnvelope/Penvsustain': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FreqEnvelope/Penvstretch': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FreqEnvelope/PA_dt': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FreqEnvelope/PA_val': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FreqEnvelope/PD_dt': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FreqEnvelope/PD_val': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FreqEnvelope/PS_val': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FreqEnvelope/PR_dt': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FreqEnvelope/PR_val': {'type': 'i'},
        '/kit0/adpars/GlobalPar/AmpEnvelope/Penvpoints': {'type': 'i'},
        '/kit0/adpars/GlobalPar/AmpEnvelope/Penvsustain': {'type': 'i'},
        '/kit0/adpars/GlobalPar/AmpEnvelope/Penvstretch': {'type': 'i'},
        '/kit0/adpars/GlobalPar/AmpEnvelope/PA_dt': {'type': 'i'},
        '/kit0/adpars/GlobalPar/AmpEnvelope/PA_val': {'type': 'i'},
        '/kit0/adpars/GlobalPar/AmpEnvelope/PD_dt': {'type': 'i'},
        '/kit0/adpars/GlobalPar/AmpEnvelope/PD_val': {'type': 'i'},
        '/kit0/adpars/GlobalPar/AmpEnvelope/PS_val': {'type': 'i'},
        '/kit0/adpars/GlobalPar/AmpEnvelope/PR_dt': {'type': 'i'},
        '/kit0/adpars/GlobalPar/AmpEnvelope/PR_val': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FilterEnvelope/Penvpoints': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FilterEnvelope/Penvsustain': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FilterEnvelope/Penvstretch': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FilterEnvelope/PA_dt': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FilterEnvelope/PA_val': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FilterEnvelope/PD_dt': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FilterEnvelope/PD_val': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FilterEnvelope/PS_val': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FilterEnvelope/PR_dt': {'type': 'i'},
        '/kit0/adpars/GlobalPar/FilterEnvelope/PR_val': {'type': 'i'},
        '/kit0/adpars/GlobalPar/GlobalFilter/Pcategory': {'type': 'i'},
        '/kit0/adpars/GlobalPar/GlobalFilter/Ptype': {'type': 'i'},
        '/kit0/adpars/GlobalPar/GlobalFilter/Pfreq': {'type': 'i'},
        '/kit0/adpars/GlobalPar/GlobalFilter/Pq': {'type': 'i'},
        '/kit0/adpars/GlobalPar/GlobalFilter/Pstages': {'type': 'i'},
        '/kit0/adpars/GlobalPar/GlobalFilter/Pfreqtrack': {'type': 'i'},
        '/kit0/adpars/GlobalPar/GlobalFilter/Pgain': {'type': 'i'},
        '/kit0/adpars/GlobalPar/GlobalFilter/Pnumformants': {'type': 'i'},
        '/kit0/adpars/GlobalPar/GlobalFilter/Pformantslowness': {'type': 'i'},
        '/kit0/adpars/GlobalPar/GlobalFilter/Pvowelclearness': {'type': 'i'},
        '/kit0/adpars/GlobalPar/GlobalFilter/Pcenterfreq': {'type': 'i'},
        '/kit0/adpars/GlobalPar/GlobalFilter/Poctavesfreq': {'type': 'i'},
        '/kit0/adpars/GlobalPar/GlobalFilter/Psequencesize': {'type': 'i'},
        '/kit0/adpars/GlobalPar/GlobalFilter/Psequencestretch': {'type': 'i'},
        '/kit0/adpars/GlobalPar/PDetune': {'type': 'i'},
        '/kit0/adpars/GlobalPar/PCoarseDetune': {'type': 'i'},
        '/kit0/adpars/GlobalPar/PDetuneType': {'type': 'i'},
        '/kit0/adpars/GlobalPar/PBandwidth': {'type': 'i'},
        '/kit0/adpars/GlobalPar/PPanning': {'type': 'i'},
        '/kit0/adpars/GlobalPar/PVolume': {'type': 'i'},
        '/kit0/adpars/GlobalPar/PAmpVelocityScaleFunction': {'type': 'i'},
        '/kit0/adpars/GlobalPar/PPunchStrength': {'type': 'i'},
        '/kit0/adpars/GlobalPar/PPunchTime': {'type': 'i'},
        '/kit0/adpars/GlobalPar/PPunchStretch': {'type': 'i'},
        '/kit0/adpars/GlobalPar/PPunchVelocitySensing': {'type': 'i'},
        '/kit0/adpars/GlobalPar/PFilterVelocityScale': {'type': 'i'},
        '/kit0/adpars/GlobalPar/PFilterVelocityScaleFunction': {'type': 'i'},
        '/kit0/adpars/GlobalPar/octave': {'type': 'i'},
        '/kit0/adpars/GlobalPar/coarsedetune': {'type': 'i'}
    }
