from xml.dom import minidom
from HFSetting import HFSetting
import os
import ROOT as r

rbxDir = "output/HFPhaseScan_July01-2015_5050/delay/"
ttcrxPath = "output/HFPhaseScan_July01-2015_5050/ttcrx.xml"
outDirPath = "check/2015-July-01-DelaySetting.root"


# rbxDir = "Data/20150521_HFPhaseScan_Shift0_Edmund/delay/"
# ttcrxPath = "Data/20150521_HFPhaseScan_Shift0_Edmund/ttcrx.xml"
# outDirPath = "check/2015-May-21-DelaySetting.root"

mapPath = "Data/2015-may-4_HCALmapHBEF_G_uHTR.txt"

# =============================================
# Read setting from xml files
# =============================================

brick_in_paths = [ rbxDir + "/" + p for p in os.listdir(rbxDir) if os.path.isfile(os.path.join(rbxDir,p)) and p.endswith(".xml") and not p.startswith(".") ]

delaySetting = {}
xmlFiles = {}
for brickPath in brick_in_paths:
	rbxName = brickPath.split("/")[-1][:5]
	xmlFiles[rbxName] = minidom.parse(brickPath)
	data = xmlFiles[rbxName].getElementsByTagName("Data")
	for datum in data:
		delaySetting[ ( rbxName,int(datum.getAttribute("qie")),int(datum.getAttribute("rm")),int(datum.getAttribute("card"))  ) ] = int(datum.childNodes[0].nodeValue)

ttcrxSetting = {}
ttcrxFile = minidom.parse(ttcrxPath)
data = ttcrxFile.getElementsByTagName("Data")
for datum in data:
	ttcrxSetting[str(datum.getAttribute("id"))] = datum.childNodes[0].nodeValue


# =============================================
# Read mapping from lmap
# =============================================

mapping = HFSetting(mapPath)

# =============================================
# Produce histograms
# =============================================

outFile = r.TFile(outDirPath,"RECREATE")
hist_depth1 = r.TH2D("depth1"," Depth 1 ; i#eta ; i#phi ", 85, -42.5, 42.5, 72, 0.5, 72.5 )
hist_depth2 = r.TH2D("depth2"," Depth 2 ; i#eta ; i#phi ", 85, -42.5, 42.5, 72, 0.5, 72.5 )

for channel,delay in delaySetting.iteritems():
	if channel[2] == 4: continue
	mapCoord =  mapping.inverse_map[channel]
	if mapCoord[2] == 1:
		hist_depth1.SetBinContent( hist_depth1.GetXaxis().FindBin(mapCoord[0]) ,  hist_depth1.GetYaxis().FindBin(mapCoord[1])  ,  delay   )
	elif mapCoord[2] == 2:
		hist_depth2.SetBinContent( hist_depth2.GetXaxis().FindBin(mapCoord[0]) ,  hist_depth2.GetYaxis().FindBin(mapCoord[1])  ,  delay   )

hist_depth1.Write()
hist_depth2.Write()

outFile.Close()































