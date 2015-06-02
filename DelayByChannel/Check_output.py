from xml.dom import minidom
import os
import ROOT as r
from HFSetting import HFSetting

original_brick_path = "Data/2015-may-12/"
adjust_brick_path = "2015-june-1_Delays_5050/"
require_setting_path = "Data/20150528_RelativeTimeShift.root"
emapFile = "Data/emap.txt"
plotFileName = "output/20150531_HFPhaseScan.root"
print_each_channel = False
makePlot = True

#==============================================================================================
# Get path for each xml files
#==============================================================================================
original_brick_paths = [ original_brick_path + "/" + p for p in os.listdir(original_brick_path) if os.path.isfile(os.path.join(original_brick_path,p)) and p.startswith("HF") and p.endswith(".xml") and not p.startswith("TTcrx") ]
original_ttcrx_path = original_brick_path+"TTcrx_DELAY.xml"

adjust_brick_paths = [ adjust_brick_path + "/" + p for p in os.listdir(adjust_brick_path) if os.path.isfile(os.path.join(adjust_brick_path,p)) and p.startswith("HF") and p.endswith(".xml") and not p.startswith("TTcrx") ]
adjust_ttcrx_path = adjust_brick_path+"TTcrx_DELAY.xml"

#==============================================================================================
# Read setting for each channel
#==============================================================================================
original_setting = {}
adjust_setting = {}
require_setting = {}

for brick_path in original_brick_paths:
	rbxName = brick_path.split("/")[-1][:5]
	original_setting[rbxName] = {}
	xmlFile = minidom.parse(brick_path)
	data = xmlFile.getElementsByTagName("Data")
	for datum in data:
		original_setting[rbxName][ ( int(datum.getAttribute("qie")),int(datum.getAttribute("rm")),int(datum.getAttribute("card"))  ) ] = int(datum.childNodes[0].nodeValue)

for brick_path in adjust_brick_paths:
	rbxName = brick_path.split("/")[-1][:5]
	adjust_setting[rbxName] = {}
	xmlFile = minidom.parse(brick_path)
	data = xmlFile.getElementsByTagName("Data")
	for datum in data:
		adjust_setting[rbxName][ ( int(datum.getAttribute("qie")),int(datum.getAttribute("rm")),int(datum.getAttribute("card"))  ) ] = int(datum.childNodes[0].nodeValue)

histFile = r.TFile(require_setting_path,"READ")
histos = {
	1:  histFile.Get("shift_depth1"),
	2:  histFile.Get("shift_depth2")
}
hfSetting = HFSetting(emapFile)

for EtaPhi_channel,RBX_channel in hfSetting.map().iteritems():
	if RBX_channel[0] not in require_setting:
		require_setting[RBX_channel[0]] = {}
	require_setting[RBX_channel[0]][(RBX_channel[1],RBX_channel[2],RBX_channel[3])] = histos[EtaPhi_channel[2]].GetBinContent( histos[EtaPhi_channel[2]].GetXaxis().FindBin(EtaPhi_channel[0]) ,  histos[EtaPhi_channel[2]].GetYaxis().FindBin(EtaPhi_channel[1]))



#==============================================================================================
# check setting for each channel
#==============================================================================================
channel_diff = []
calibration_check = []
in_range = []
for rbxName,channels in original_setting.iteritems():
	if len(original_setting[rbxName]) != len(adjust_setting[rbxName]):
		print "number of channels for %s are different for the two settings!"
	for channel,delay in channels.iteritems():
		if channel in adjust_setting[rbxName]:
			if print_each_channel:
				print "======================================================"
				print "%s channel qie %s, rm %s, card %s setting:"%(rbxName,channel[0],channel[1],channel[2])
				print "original setting: %s"%delay
				print "adjust setting: %s"%adjust_setting[rbxName][channel]
			if channel[1] != 4:
				if print_each_channel:
					print "require adjust setting: %s"%require_setting[rbxName][channel]
				channel_diff.append((adjust_setting[rbxName][channel] - delay - int(require_setting[rbxName][channel])))
				in_range.append( adjust_setting[rbxName][channel] <= 24 and adjust_setting[rbxName][channel] >= 0 )  
			else:
				if print_each_channel:
					print "this is a calibration channel with rm = 4"
				calibration_check.append( adjust_setting[rbxName][channel] == 0 and delay == 0 )

		else:
			print "%s channel qie %s, rm %s, card %s not found in adjust setting"%(channel[0],channel[1],channel[2],channel[3])


#==============================================================================================
# make plot for global shift number
#==============================================================================================
# plotFile = r.TFile(plotFileName,"RECREATE")
# delay_hist = r.TH2F("delay_hist","Delay Distribution for all channels ; [ns] ; ",100,-50,50)




print "Are all the non-calibration setting consistent? ", all([diff == 0 for diff in channel_diff])
print "Are all non-calibration setting in range? ", all(in_range)
print "Are all the calibration setting zero? ", all(calibration_check)
