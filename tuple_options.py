from Configurables import DecayTreeTuple
from DecayTreeTuple.Configuration import *
from Configurables import DaVinci
from GaudiConf import IOHelper

# Stream and stripping line we want to use
stream = 'AllStreams'
line = 'D2hhCompleteEventPromptDst2D2RSLine'

# Create an ntuple to capture D*+ decays from the StrippingLine line
dtt = DecayTreeTuple('TupleDstToD0pi_D0ToKpi')
dtt.Inputs = ['/Event/{0}/Phys/{1}/Particles'.format(stream, line)]
dtt.Decay = '[D*(2010)+ -> ^(D0 -> ^K- ^pi+) pi+]CC'

track_tool = dtt.addTupleTool('TupleToolTrackInfo')
dtt.addTupleTool('TupleToolPrimaries')

# Add Branches
dtt.addBranches({'Dstar' : '[D*(2010)+ -> (D0 -> K- pi+) pi+]CC',
                 'D0'    : '[D*(2010)+ -> ^(D0 -> K- pi+) pi+]CC',
                 'Kminus': '[D*(2010)+ -> (D0 -> ^K- pi+) pi+]CC',
                 'piplus': '[D*(2010)+ -> (D0 -> K- ^pi+) pi+]CC',
                 'pisoft': '[D*(2010)+ -> (D0 -> K- pi+) ^pi+]CC'})

dtt.D0.addTupleTool('TupleToolPropertime')

# Add some functors
dstar_hybrid = dtt.Dstar.addTupleTool('LoKi::Hybrid::TupleTool/LoKi_Dstar')
d0_hybrid = dtt.D0.addTupleTool('LoKi::Hybrid::TupleTool/LoKi_D0')
pisoft_hybrid = dtt.pisoft.addTupleTool('LoKi::Hybrid::TupleTool/LoKi_PiSoft')

# Define Functors in preambulo
preamble = [
    'DZ = VFASPF(VZ) - BPV(VZ)',
    'TRACK_MAX_PT = MAXTREE(ISBASIC & HASTRACK, PT, -1)'
]
dstar_hybrid.Preambulo = preamble
d0_hybrid.Preambulo = preamble

# Define Branches with functors
dstar_hybrid.Variables = {
    'mass': 'MM',
    'mass_D0': 'CHILD(MM, 1)',
    'pt': 'PT',
    'dz': 'DZ',
    'dira': 'BPVDIRA',
    'max_pt': 'MAXTREE(ISBASIC & HASTRACK, PT, -1)',
    'max_pt_preambulo': 'TRACK_MAX_PT',
    'sum_pt_pions': 'SUMTREE(211 == ABSID, PT)',
    'n_highpt_tracks': 'NINTREE(ISBASIC & HASTRACK & (PT > 1500*MeV))'
}
d0_hybrid.Variables = {
    'mass': 'MM',
    'pt': 'PT',
    'dira': 'BPVDIRA',
    'vtx_chi2': 'VFASPF(VCHI2)',
    'dz': 'DZ'
}
pisoft_hybrid.Variables = {
    'p': 'P',
    'pt': 'PT'
}

# Configure DecayTreeFitter
dtt.addBranches({
    'Dstar': '[D*(2010)+ -> (D0 -> K- pi+) pi+]CC',
})

dtt.Dstar.addTupleTool('TupleToolDecayTreeFitter/ConsD')

dtt.Dstar.ConsD.constrainToOriginVertex = True
dtt.Dstar.ConsD.Verbose = True
dtt.Dstar.ConsD.daughtersToConstrain = ['D0']

# Configure DaVinci
DaVinci().UserAlgorithms += [dtt]
DaVinci().InputType = 'DST'
DaVinci().TupleFile = 'DVntuple.root'
DaVinci().PrintFreq = 1000
DaVinci().DataType = '2012'
DaVinci().Simulation = True
# Only ask for luminosity information when not using simulated data
DaVinci().Lumi = not DaVinci().Simulation
DaVinci().EvtMax = -1
DaVinci().CondDBtag = 'sim-20130522-1-vc-md100'
DaVinci().DDDBtag = 'dddb-20130929-1'

# Use the local input data
IOHelper().inputFiles([
    './00035742_00000001_1.allstreams.dst'
], clear=True)
