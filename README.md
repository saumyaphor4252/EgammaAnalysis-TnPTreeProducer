### Datasets used
```
/RelValZEE_14/CMSSW_14_2_0-PU_142X_mcRun3_2025_realistic_v4_Winter25_PU_RV255_2-v1/MINIAODSIM 116000
/RelValZEE_14/CMSSW_14_2_0-PU_142X_mcRun3_2025_realistic_v4_Winter25_PU_RV255_2-v2/MINIAODSIM 120000
/RelValZEE_14/CMSSW_14_2_0-PU_142X_mcRun3_2025_realistic_v4_Winter25_PU_RV255_2-v3/MINIAODSIM 120000
/RelValZEE_14/CMSSW_14_2_0-PU_142X_mcRun3_2025_realistic_v4_Winter25_PU_RV255_2-v4/MINIAODSIM 120000
/RelValZEE_14/CMSSW_14_2_0-PU_142X_mcRun3_2025_realistic_v4_Winter25_PU_RV255_6-v1/MINIAODSIM 134200
/RelValZEE_14/CMSSW_14_2_0-PU_142X_mcRun3_2025_realistic_v4_Winter25_PU_RV255_7-v1/MINIAODSIM 134300
/RelValZEE_14/CMSSW_14_2_0-PU_142X_mcRun3_2025_realistic_v4_Winter25_PU_RV255_8-v1/MINIAODSIM 131800
/RelValZEE_14/CMSSW_14_2_0-PU_142X_mcRun3_2025_realistic_v4_Winter25_PU_RV255_9-v1/MINIAODSIM 134600
/RelValZEE_14/CMSSW_14_2_0-PU_142X_mcRun3_2025_realistic_v4_Winter25_PU_RV255_10-v1/MINIAODSIM 132000
/RelValZEE_14/CMSSW_14_2_0-PU_142X_mcRun3_2025_realistic_v4_Winter25_PU_RV255_11-v1/MINIAODSIM 134600
/RelValZEE_14/CMSSW_14_2_0-PU_142X_mcRun3_2025_realistic_v4_Winter25_PU_RV255_12-v1/MINIAODSIM 134300
```
#### Set up rucio rules for the datasets if needed:
```
voms-proxy-init --voms cms
source /cvmfs/cms.cern.ch/rucio/setup-py3.sh
rucio add-rule cms:/RelValZEE_14/CMSSW_14_2_0-PU_142X_mcRun3_2025_realistic_v4_Winter25_PU_RV255_2-v1/MINIAODSIM 1 T2_CH_CERN  --lifetime 864000 --comment "Needed for urgent feedback on Winter25 samples"
rucio add-rule cms:/RelValZEE_14/CMSSW_14_2_0-PU_142X_mcRun3_2025_realistic_v4_Winter25_PU_RV255_2-v2/MINIAODSIM 1 T2_CH_CERN  --lifetime 864000 --comment "Needed for urgent feedback on Winter25 samples"
rucio add-rule cms:/RelValZEE_14/CMSSW_14_2_0-PU_142X_mcRun3_2025_realistic_v4_Winter25_PU_RV255_2-v3/MINIAODSIM 1 T2_CH_CERN  --lifetime 864000 --comment "Needed for urgent feedback on Winter25 samples"
rucio add-rule cms:/RelValZEE_14/CMSSW_14_2_0-PU_142X_mcRun3_2025_realistic_v4_Winter25_PU_RV255_2-v4/MINIAODSIM 1 T2_CH_CERN  --lifetime 864000 --comment "Needed for urgent feedback on Winter25 samples"
rucio add-rule cms:/RelValZEE_14/CMSSW_14_2_0-PU_142X_mcRun3_2025_realistic_v4_Winter25_PU_RV255_6-v1/MINIAODSIM 1 T2_CH_CERN  --lifetime 864000 --comment "Needed for urgent feedback on Winter25 samples"
rucio add-rule cms:/RelValZEE_14/CMSSW_14_2_0-PU_142X_mcRun3_2025_realistic_v4_Winter25_PU_RV255_7-v1/MINIAODSIM 1 T2_CH_CERN  --lifetime 864000 --comment "Needed for urgent feedback on Winter25 samples"
rucio add-rule cms:/RelValZEE_14/CMSSW_14_2_0-PU_142X_mcRun3_2025_realistic_v4_Winter25_PU_RV255_8-v1/MINIAODSIM 1 T2_CH_CERN  --lifetime 864000 --comment "Needed for urgent feedback on Winter25 samples"
rucio add-rule cms:/RelValZEE_14/CMSSW_14_2_0-PU_142X_mcRun3_2025_realistic_v4_Winter25_PU_RV255_9-v1/MINIAODSIM 1 T2_CH_CERN  --lifetime 864000 --comment "Needed for urgent feedback on Winter25 samples"
rucio add-rule cms:/RelValZEE_14/CMSSW_14_2_0-PU_142X_mcRun3_2025_realistic_v4_Winter25_PU_RV255_10-v1/MINIAODSIM 1 T2_CH_CERN  --lifetime 864000 --comment "Needed for urgent feedback on Winter25 samples"
rucio add-rule cms:/RelValZEE_14/CMSSW_14_2_0-PU_142X_mcRun3_2025_realistic_v4_Winter25_PU_RV255_11-v1/MINIAODSIM 1 T2_CH_CERN  --lifetime 864000 --comment "Needed for urgent feedback on Winter25 samples"
rucio add-rule cms:/RelValZEE_14/CMSSW_14_2_0-PU_142X_mcRun3_2025_realistic_v4_Winter25_PU_RV255_12-v1/MINIAODSIM 1 T2_CH_CERN  --lifetime 864000 --comment "Needed for urgent feedback on Winter25 samples"
```
### Set-up for ntuples
```
cmsrel CMSSW_14_2_0
cd CMSSW_14_2_0/src
cmsenv
git clone -b 140X_Tracker2025Scenarios git@github.com: EgammaAnalysis/TnPTreeProducer
scram b -j 10
cd EgammaAnalysis-TnPTreeProducer/
### Do a local test of configurations
cd python/
cmsRun TnPTreeProducer_cfg.py isMC=True doTrigger=True era=2025
### If runs without issues, move to crab submission
cd ../crab/
python3 tnpCrabSubmit_Winter25.py
### This will create the configurations for crab submission
crab submit crab_submit_ZEE_RV255_10-v1.py
```
### Plotting 
