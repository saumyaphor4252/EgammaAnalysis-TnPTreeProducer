#!/bin/env python
import os

#
# Example script to submit TnPTreeProducer to crab
#
submitVersion = "2024-10-28" # add some date here
doL1matching  = False
isAOD = False

defaultArgs   = ['doEleID=False','doPhoID=False','doTrigger=True']
mainOutputDir = '/store/group/phys_egamma/ssaumya/Tracker2025Scenarios/%s' % (submitVersion)

# Logging the current version of TnpTreeProducer here, such that you can find back what the actual code looked like when you were submitting
os.system('mkdir -p /eos/cms/%s' % mainOutputDir)
os.system('(git log -n 1;git diff) &> /eos/cms/%s/git.log' % mainOutputDir)


#
# Common CRAB settings
#
from CRABClient.UserUtilities import config
config = config()

config.General.requestName             = ''
config.General.transferLogs            = False
config.General.workArea                = 'crab_%s' % submitVersion

config.JobType.pluginName              = 'Analysis'
config.JobType.psetName                = '../python/TnPTreeProducer_cfg.py'
config.JobType.sendExternalFolder      = True
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset               = ''
config.Data.inputDBS                   = 'global'
config.Data.publication                = False
config.Data.allowNonValidInputDataset  = True
config.Site.storageSite                = 'T2_CH_CERN'


#
# Certified lumis for the different eras
#   (seems the JSON for UL2017 is slightly different from rereco 2017, it's not documented anywhere though)
#
def getLumiMask(era):
  if   era=='2016':   return 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
  elif era=='2017':   return 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'
  elif era=='2018':   return 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/PromptReco/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'
  elif era=='UL2016preVFP': return 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'
  elif era=='UL2016postVFP': return 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'
  elif era=='UL2017': return 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt'
  elif era=='UL2018': return 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/PromptReco/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'
  elif era=='2022': return 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions22/Cert_Collisions2022_355100_362760_Golden.json'
  elif era=='2023': return 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json'
  #elif era=='2024': return 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions24/Cert_Collisions2024_378981_379470_Golden.json'

#
# Submit command
#
from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from http.client import HTTPException

crab_sub = open("crab_sub.sh", "w")
crab_status = open("crab_status.sh", "w")
crab_resub = open("crab_resub.sh", "w")
crab_merge = open("crab_merge.sh", "w")
path = "/eos/cms/store/group/phys_egamma/ssaumya/Tracker2025Scenarios/tnpTuples/"

def submit(config, requestName, sample, era, json, extraParam=[]):
  isMC                        = 'SIM' in sample
  dMC = "data"
  if isMC: dMC = "mc"
  config.General.requestName  = '%s_%s' % (dMC, requestName)
  config.Data.inputDataset    = sample
  config.Data.outLFNDirBase   = '%s/%s/%s/' % (mainOutputDir, era, dMC)
  config.Data.splitting       = 'FileBased' if isMC else 'LumiBased'
  config.Data.lumiMask        = None if isMC else json
  config.Data.unitsPerJob     = 5 if isMC else 20
  config.JobType.pyCfgParams  = defaultArgs + ['isMC=True' if isMC else 'isMC=False', 'era=%s' % era] + extraParam
  outF = open('crab_submit_%s.py'%requestName, 'w')
  #outF.write(config)
  print( config, file=outF)
  outF.close()
  crab_sub.write("crab submit crab_submit_%s.py \n"%requestName)
  crab_status.write("crab status -d crab_%s/crab_%s_%s \n"%(submitVersion, dMC, requestName))
  crab_resub.write("crab resubmit -d crab_%s/crab_%s_%s \n"%(submitVersion, dMC, requestName))
  haddIn = "%s/%s/%s/%s/%s/crab_%s_%s/*/*/*.root"%(path, submitVersion, era, dMC, sample.split("/")[1], dMC, requestName)
  haddOut = "%s/%s/%s_%s.root"%(path, submitVersion, dMC, requestName)
  print(haddOut)
  crab_merge.write('hadd -f %s %s & \n\n'%(haddOut, haddIn))
  #try:                           crabCommand('submit', config = config)
  #except HTTPException as hte:   print( "Failed submitting task: %s" % (hte.headers))
  #except ClientException as cle: print( "Failed submitting task: %s" % (cle))

#
# Wrapping the submit command
# In case of doL1matching=True, vary the L1Threshold and use sub-json
#
from multiprocessing import Process
def submitWrapper(requestName, sample, era, extraParam=[]):
  if doL1matching:
    from getLeg1ThresholdForDoubleEle import getLeg1ThresholdForDoubleEle
    for leg1Threshold, json in getLeg1ThresholdForDoubleEle(era.replace("UL","").replace("preVFP","").replace("postVFP","")):
      print( 'Submitting for leg 1 threshold %s' % (leg1Threshold))
      p = Process(target=submit, args=(config, '%s_leg1Threshold%s' % (requestName, leg1Threshold), sample, era, json, extraParam + ['L1Threshold=%s' % leg1Threshold]))
      p.start()
      p.join()
  else:
    p = Process(target=submit, args=(config, requestName, sample, era, getLumiMask(era), extraParam))
    p.start()
    p.join()
    #submit(config, requestName, sample, era, getLumiMask(era), extraParam) # print the config files

#
# List of samples to submit, with eras
# Here the default data/MC for UL and rereco are given (taken based on the release environment)
# If you would switch to AOD, don't forget to add 'isAOD=True' to the defaultArgs!
#
#from EgammaAnalysis.TnPTreeProducer.cmssw_version import isReleaseAbove
#if isReleaseAbove(13,0):

eraMC_2024 = '2024'
eraMC_2024_TkDPGv2 = '2024_EOR3_TkDPGv2'
eraMC_2024_TkDPGv6 = '2024_EOR3_TkDPGv6'

submitWrapper('ZEE_Reference', '/RelValZEE_14/CMSSW_14_0_9-PU_140X_mcRun3_2024_realistic_v14_RV245_2024-v1/MINIAODSIM', eraMC_2024)
submitWrapper('ZEE_EOR3_TkDPGv2', '/RelValZEE_14/CMSSW_14_0_9-PU_140X_mcRun3_2024_realistic_EOR3_TkDPGv2_RV245_2024-v4/MINIAODSIM', eraMC_2024_TkDPGv2)
submitWrapper('ZEE_EOR3_TkDPGv6', '/RelValZEE_14/CMSSW_14_0_9-PU_140X_mcRun3_2024_realistic_EOR3_TkDPGv6_RV245_2024-v1/MINIAODSIM', eraMC_2024_TkDPGv6)
