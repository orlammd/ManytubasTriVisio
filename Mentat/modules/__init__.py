from sys import argv

from mentat import Engine, Module

from .raysession import RaySession
from .openstagecontrol import OpenStageControl
from .pedalboard import PedalBoard
from .transport import Transport
#from .microtonality import MicroTonality
from .postprocess import PostProcess
#from .calfmonosynth import CalfMonoSynth, CalfPitcher
#from .autotune import Autotune
#from .klick import Klick
#from .sooperlooper import SooperLooper
#from .loop192 import Loop192
#from .seq192 import Seq192
from .nonmixer import NonMixer
#from .nonmixers import *
#from .zynaddsubfx import ZynAddSubFx, ZynPart
from .tap192 import Tap192
#from .mk2minilab import Mk2Control, Mk2Keyboard
#from .jmjkeyboard import JmjKeyboard
#from .joystick import Joystick


"""
Engine
"""
engine = Engine('Mentat', 2001, '/home/plagiat/PlagiatSetup/Mentat', tcp_port=55001, debug='--debug' in argv)
raysession = RaySession('RaySession', 'osc', 2000)


"""
Controllers
"""
openstagecontrol = OpenStageControl('OpenStageControl', 'osc', 3000)
openstagecontrolKeyboardOut = Module('OpenStageControlKeyboardOut', 'midi')
pedalboard = PedalBoard('PedalBoard', 'osc', 3001)
#jmjKeyboard = JmjKeyboard('JmjKeyboard', 'osc', 3002)
#mk2Keyboard = Mk2Keyboard('Mk2Keyboard', 'osc', 3003)
#mk2Control = Mk2Control('Mk2Control', 'midi')
#joystick = Joystick('Joystick', 'osc', 3004)


"""
Loopers
"""
#looper = SooperLooper('AudioLooper', 'osc', 9951)
#loop192 = Loop192('Loop192', 'osc', 9910)

"""
Sequencers
"""
#klick = Klick('Klick', 'osc', 9800)
#seq192 = Seq192('Seq192', 'osc', 9920)

"""
Mixers
"""
inputs = NonMixer('Inputs', 'osc', 10000)
outputs = NonMixer('Outputs', 'osc', 10001)
# monitorsNano = NonMixer('MonitorsNano', 'osc', 10002)
# monitorsKesch = NonMixer('MonitorsKesch', 'osc', 10003)
#
# bass = NonMixer('Bass', 'osc', 10010)
# bassFX = bassfx = BassFX('BassFX', 'osc', 10011)
#
# bassSynths = NonMixer('BassSynths', 'osc', 10020)
#
# synths = NonMixer('Synths', 'osc', 10030)
# synthsFX1Reverb = NonMixer('SynthsFX1Reverb', 'osc', 10031)
# synthsFX2Delay = NonMixer('SynthsFX2Delay', 'osc', 10032)
# synthsFX3Delay = NonMixer('SynthsFX3Delay', 'osc', 10033)
# synthsFX4TapeDelay = NonMixer('SynthsFX4TapeDelay', 'osc', 10034)
# synthsFX5Scape = NonMixer('SynthsFX5Scape', 'osc', 10035)
#
# samples = NonMixer('Samples', 'osc', 10040)
# samplesFX1Delay = NonMixer('SamplesFX1Delay', 'osc', 10041)
# samplesFX2Delay = NonMixer('SamplesFX2Delay', 'osc', 10042)
# samplesFX3Reverb = NonMixer('SamplesFX3Reverb', 'osc', 10043)
# samplesFX4Autofilter = NonMixer('SamplesFX4Autofilter', 'osc', 10044)
# samplesFX5TapeDelay = NonMixer('SamplesFX5TapeDelay', 'osc', 10045)
# samplesFX6Scape = NonMixer('SamplesFX6Scape', 'osc', 10046)
# samplesFX7Degrade = NonMixer('SamplesFX7Degrade', 'osc', 10047)
#
# vocalsNano = Vocals('VocalsNano', 'osc', 10050)
# vocalsNanoFX1Delay = NonMixer('VocalsNanoFX1Delay', 'osc', 10051)
# vocalsNanoFX2Delay = NonMixer('VocalsNanoFX2Delay', 'osc', 10052)
# vocalsNanoFX3TrapVerb = NonMixer('VocalsNanoFX3TrapVerb', 'osc', 10053)
# vocalsNanoFX4Disint = NonMixer('VocalsNanoFX4Disint', 'osc', 10054)
# vocalsNanoFX5RingMod = NonMixer('VocalsNanoFX5RingMod', 'osc', 10055)
# vocalsNanoFX6Granular = NonMixer('VocalsNanoFX6Granular', 'osc', 10056)
# vocalsNanoFX7Slice = NonMixer('VocalsNanoFX7Slice', 'osc', 10057)
# vocalsNanoFX8TapeDelay = NonMixer('VocalsNanoFX8TapeDelay', 'osc', 10058)
# vocalsNanoFX8Scape = NonMixer('VocalsNanoFX9Scape', 'osc', 10059)
#
# vocalsKesch = Vocals('VocalsKesch', 'osc', 10060)
# vocalsKeschFX1Delay = NonMixer('VocalsKeschFX1Delay', 'osc', 10061)
# vocalsKeschFX2Delay = NonMixer('VocalsKeschFX2Delay', 'osc', 10062)
# vocalsKeschFX3TrapVerb = NonMixer('VocalsKeschFX3TrapVerb', 'osc', 10063)
# vocalsKeschFX4Disint = NonMixer('VocalsKeschFX4Disint', 'osc', 10064)
# vocalsKeschFX5RingMod = NonMixer('VocalsKeschFX5RingMod', 'osc', 10065)
# vocalsKeschFX6Granular = NonMixer('VocalsKeschFX6Granular', 'osc', 10066)
# vocalsKeschFX7Slice = NonMixer('VocalsKeschFX7Slice', 'osc', 10067)
# vocalsKeschFX8TapeDelay = NonMixer('VocalsKeschX8TapeDelay', 'osc', 10068)
# vocalsKeschFX8Scape = NonMixer('VocalsKeschFX9Scape', 'osc', 10069)

"""
Samplers
"""
prodSampler = Tap192('ProdSampler', 'osc', 11040)
#constantSampler = Tap192('ConstantSampler', 'osc', 11041)

"""
Synths
"""
# carlabass = Module('LowCSynths', 'osc', 9720)
# carlabass.add_submodule(
#     CalfMonoSynth('LowCTrap1', parent=carlabass),
#     CalfMonoSynth('LowCTrap2', parent=carlabass),
#     CalfMonoSynth('LowCBarkline', parent=carlabass),
#     CalfMonoSynth('LowCBoom', parent=carlabass),
# )
#
# carlatreble = Module('HiCSynths', 'osc', 9730)
# carlatreble.add_submodule(
#     CalfMonoSynth('CRhodes', parent=carlatreble),
#     CalfMonoSynth('CDubstepHorn', parent=carlatreble),
#     CalfMonoSynth('CTrap', parent=carlatreble),
#     CalfMonoSynth('CEasyClassical', parent=carlatreble),
# )
# calfpitcher = CalfPitcher('CalfPitcher', 'osc', 9740)
#
#
# zynbass =  ZynAddSubFx('ZLowSynths', 'osc', 9820)
# zynbass.add_submodule(
#     ZynPart('LowZDubstep', parent=zynbass, parts=[0]),
#     ZynPart('LowZDancestep', parent=zynbass, parts=[1]),
#     ZynPart('LowZRagstep', parent=zynbass, parts=[2]),
#     ZynPart('LowZDupieux', parent=zynbass, parts=[3]),
#     ZynPart('LowZPhrampton', parent=zynbass, parts=[4])
# )
#
# zyntreble =  ZynAddSubFx('ZHiSynths', 'osc', 9830)
# zyntreble.add_submodule(
#     ZynPart('ZDupieux', parent=zyntreble, parts=[0]),
#     ZynPart('ZNotSoRhodes', parent=zyntreble, parts=[1]),
#     ZynPart('ZOrgan', parent=zyntreble, parts=[2, 3]),
#     ZynPart('ZCosma', parent=zyntreble, parts=[4]),
#     ZynPart('ZBombarde', parent=zyntreble, parts=[5]),
#     ZynPart('ZTrumpets', parent=zyntreble, parts=[6, 7, 8]),
#     ZynPart('ZStambul', parent=zyntreble, parts=[9]),
#     ZynPart('ZDre', parent=zyntreble, parts=[10]),
#     ZynPart('ZDiploLike', parent=zyntreble, parts=[11]),
#     ZynPart('ZJestoProunk', parent=zyntreble, parts=[12]),
#     ZynPart('Z8bits', parent=zyntreble, parts=[13, 14])
# )


"""
Autotunes
"""
# autotuneNanoMeuf = Autotune('NanoMeuf', 'osc', 12050, offset=4.0)
# autotuneNanoNormo = Autotune('NanoNormo', 'osc', 12051, offset=0.0)
# autotuneNanoGars = Autotune('NanoGars', 'osc', 12052, offset=-4.0)
#
# autotuneKeschMeuf = Autotune('KeschMeuf', 'osc', 12061, offset=4.0)
# autotuneKeschNormo = Autotune('KeschNormo', 'osc', 12060, offset=0.0)
# autotuneKeschGars = Autotune('KeschGars', 'osc', 12062, offset=-4.0)


"""
Miscellaneous
"""
#microtonality = MicroTonality('MicroTonality')
transport = Transport('Transport')
postprocess = PostProcess('PostProcess')
