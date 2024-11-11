# Submission for 2024 Tracker EOR3 MC Scenarios
For Initial Set up of 2024
```
git clone -b Run3_13X git@github.com:cms-egamma/EgammaAnalysis-TnPTreeProducer.git EgammaAnalysis/TnPTreeProducer
#git clone -b 140X_Tracker2025Scenarios git@github.com:cms-egamma/EgammaAnalysis-TnPTreeProducer.git EgammaAnalysis/TnPTreeProducer
scram b -j8
```

Running and submitting jobs thereafter
```
cd /afs/cern.ch/work/s/ssaumya/private/Egamma/TrackerStudies/CMSSW_14_0_9/src/EgammaAnalysis/TnPTreeProducer/
cmsenv
scram b -j 10
cd crab
source /cvmfs/cms.cern.ch/common/crab-setup.sh
voms-proxy-init -voms cms 
# Update the tnpCrabSubmit.py as needed
python3 tnpCrabSubmit_PrivateMINIAOD.py
# This will create the crab python configurations:
# e.g. crab_submit_ZEE_Reference.py
crab submit crab_submit_ZEE_Reference.py
# For checking the job status:
# crab status -d <directory> --verboseErrors
```

