my_job = Job(application=DaVinci(version='v36r6'))
my_job.backend = Dirac()
my_job.name = 'Starterkit-Job 1'
my_job.inputdata = my_job.application.readInputData('MC_2012_27163003_Beam4000GeV2012MagDownNu2.5Pythia8_Sim08e_Digi13_Trig0x409f0045_Reco14a_Stripping20NoPrescalingFlagged_ALLSTREAMS.DST.py')
my_job.application.optsfile = ['./tuple_options.py']

