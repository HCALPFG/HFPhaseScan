

# =====================================
# Configuration file for delay setting
# =====================================

def delaySettingFiles():
	return {
		"depth1":("Data/20150528_RelativeTimeShift.root","shift_depth1"),
		"depth2":("Data/20150528_RelativeTimeShift.root","shift_depth2"),

		}

def mapFile():
	return "Data/emap.txt"

def brickDir():
	return "/afs/cern.ch/work/k/klo/hcal/PromptAnalysis/HFPhaseScan/DelayByChannel/Data/2015-may-26"

def TTCPath():
	return "/afs/cern.ch/work/k/klo/hcal/PromptAnalysis/HFPhaseScan/DelayByChannel/Data/TTCrxPhaseDelayRBX_0x187_tunedHTRs_tuned_v13m.xml"
