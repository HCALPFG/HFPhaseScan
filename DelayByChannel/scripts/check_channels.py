from compareSetting import compareSetting

inputBrickPath = "/afs/cern.ch/work/k/klo/hcal/PromptAnalysis/HFPhaseScan/DelayByChannel/Data/20150521_HFPhaseScan_Shift0_Edmund/delay/"
outputBrickPath = "/afs/cern.ch/work/k/klo/hcal/PromptAnalysis/HFPhaseScan/DelayByChannel/output/HFPhaseScan_June13-2015_5050/delay/"
mapPath = "Data/2015-may-4_HCALmapHBEF_G_uHTR.txt"

relativeTimingPath = {"depth1":("Data/20150528_RelativeTimeShift.root","shift_depth1"),"depth2":("Data/20150528_RelativeTimeShift.root","shift_depth2")}


compare = compareSetting(inputBrickPath,outputBrickPath,mapPath,relativeTimingPath)

RBXs = [
	"HFM01",
	"HFM02",
	"HFM03",
	"HFM04",
	"HFM05",
	"HFM06",
	"HFM07",
	"HFM08",
	"HFM09",
	"HFM10",
	"HFM11",
	"HFM12",
	"HFP01",
	"HFP02",
	"HFP03",
	"HFP04",
	"HFP05",
	"HFP06",
	"HFP07",
	"HFP08",
	"HFP09",
	"HFP10",
	"HFP11",
	"HFP12"		]


for RBX in RBXs:
	compare.printRBXInfo(RBX)
