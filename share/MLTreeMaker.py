#! /usr/bin/env python

# @file     MLTreeMaker.h
# @author   Joakim Olsson <joakim.olsson@cern.ch>
# @brief    Athena package to save cell images of clusters for ML training
# @date     October 2016

# Number of events
theApp.EvtMax = -1 # all events in dataset
#theApp.EvtMax = 2000 # testing
import AthenaPoolCnvSvc.ReadAthenaPool

# Input files for testing

## MC15a e vs p+- at 100 GeV (50k events for each dataset)
#svcMgr.EventSelector.InputCollections = ["/afs/cern.ch/user/j/jolsson/work/datasets/mc15_13TeV.422008.ParticleGun_single_ele_Pt100.recon.ESD.e4459_s2726_r7143/ESD.06642056._000019.pool.root.1"]
#svcMgr.EventSelector.InputCollections = ["/afs/cern.ch/user/j/jolsson/work/datasets/mc15_13TeV.422015.ParticleGun_single_pion_Pt100.recon.ESD.e4459_s2726_r7143/ESD.06642133._000031.pool.root.1"]

# MC16 pi- (testing dataset)
svcMgr.EventSelector.InputCollections = ["/eos/user/m/mswiatlo/esd/mc16_13TeV.428002.ParticleGun_single_piminus_logE0p2to2000.recon.ESD.e7279_s3411_r11281/ESD.17269624._000146.pool.root.1"]

from AthenaCommon.GlobalFlags import jobproperties
jobproperties.Global.DetDescrVersion="ATLAS-R2-2016-01-00-01" # For MC16

# Suggestion from Peter Loch to turn off local cluster calibration
from CaloRec.CaloTopoClusterFlags import jobproperties
jobproperties.CaloTopoClusterFlags.doTopoClusterLocalCalib.set_Value_and_Lock(False)
from CaloRec.CaloClusterTopoGetter import CaloClusterTopoGetter

# Setup MLTreeMaker algorithm
from AthenaCommon import CfgMgr
algSeq = CfgMgr.AthSequencer("AthAlgSeq")
algSeq += CfgMgr.MLTreeMaker(name = "MLTreeMaker",
                             TrackContainer = "InDetTrackParticles",
                             CaloClusterContainer = "CaloCalTopoClusters",
                             Prefix = "CALO",
                             ClusterEmin = 1.0,
                             ClusterEmax = 200.0,
                             EventCleaning = False,
                             Tracking = False,
                             Pileup = False,
                             EventTree = False,
                             ClusterTree = True,
                             OutputLevel = DEBUG)
algSeq.MLTreeMaker.RootStreamName = "OutputStream"

# Setup stream auditor
from AthenaCommon.AppMgr import ServiceMgr as svcMgr
if not hasattr(svcMgr, "DecisionSvc"):
    svcMgr += CfgMgr.DecisionSvc()
svcMgr.DecisionSvc.CalcStats = True
svcMgr += CfgMgr.THistSvc()
svcMgr.THistSvc.Output += ["OutputStream DATAFILE='mltree.pool.root' OPT='RECREATE'"]

# Setup up geometry needed for track extrapolation
include("RecExCond/AllDet_detDescr.py")
from AthenaCommon.CfgGetter import getService
getService("AtlasTrackingGeometrySvc")

# Configure object key store to recognize calo cells
from RecExConfig.ObjKeyStore import ObjKeyStore, objKeyStore
oks = ObjKeyStore()
oks.addStreamESD("CaloCellContainer", ["AllCalo"] )
