
import ROOT as r
from HFSetting import HFSetting

outPath = "check/20150528_RecommendedDelaySetting_depth%s.txt"
mapFile = "Data/2015-may-4_HCALmapHBEF_G_uHTR.txt"


outputFiles = {} 

fileDict= {"depth1":("Data/20150528_RelativeTimeShift.root","shift_depth1"),"depth2":("Data/20150528_RelativeTimeShift.root","shift_depth2")}

files = {}
hists = {}
mapping = HFSetting(mapFile)
for depth,inputInfo in fileDict.iteritems():
	fileName = inputInfo[0]
	histName = inputInfo[1]
	depthName = int(depth[-1])
	files[depthName] = r.TFile(fileName,"READ")
	hists[depthName] = files[depthName].Get(histName)
	outputFiles[depthName] = open(outPath%depthName,"w")

count = 0
for depth,hist in hists.iteritems():
	# 1 to avoid underflow bin and + 1 to include the last bin
	for xbin in range(1,hist.GetNbinsX()+1):
		for ybin in range(1,hist.GetNbinsY()+1):
			delay = hist.GetBinContent(xbin,ybin)
			ieta = hist.GetXaxis().GetBinCenter(xbin)
			iphi = hist.GetYaxis().GetBinCenter(ybin)	
			if ieta > 0:
				subDet = "HFP"
			elif ieta < 0:
				subDet = "HFM"
			if (int(ieta),int(iphi),depth,subDet) in mapping.map:
				rbxCoord = mapping.map[(int(ieta),int(iphi),depth,subDet)]
				textString = "Line {0} | ieta: {1} , iphi: {2} , depth: {3} ,  ".format(count,ieta,iphi,depth,delay)+"RBX: {0}, QIE: {1}, RM: {2}, Card: {3};".format(*rbxCoord)+" Recommended Delay: {0}  \n".format(delay)
				count += 1
				outputFiles[depth].write(textString)

for key,file in outputFiles.iteritems():
	file.close()

