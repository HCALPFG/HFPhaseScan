from xml.dom import minidom
import os
import ROOT as r
from HFSetting import HFSetting

original_brick_path = "Data/2015-may-26/"
adjust_brick_path = "test/"
require_setting_path = "Data/20150528_RelativeTimeShift.root"
emapFile = "Data/emap.txt"

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
	print require_setting[RBX_channel[0]][(RBX_channel[1],RBX_channel[2],RBX_channel[3])]



#==============================================================================================
# check setting for each channel
#==============================================================================================
channel_diff = []
for rbxName,channels in original_setting.iteritems():
	if len(original_setting[rbxName]) != len(adjust_setting[rbxName]):
		print "number of channels for %s are different for the two settings!"
	for channel,delay in channels.iteritems():
		if channel in adjust_setting[rbxName]:
			print "======================================================"
			print "%s channel qie %s, rm %s, card %s setting:"%(rbxName,channel[0],channel[1],channel[2])
			print "original setting: %s"%delay
			print "adjust setting: %s"%adjust_setting[rbxName][channel]
			if channel[1] != 4:
				print "require adjust setting: %s"%require_setting[rbxName][channel]
				channel_diff.append((adjust_setting[rbxName][channel] - delay - int(require_setting[rbxName][channel])))
			else:
				print "this is a calibration channel with rm = 4"
		else:
			print "%s channel qie %s, rm %s, card %s not found in adjust setting"%(channel[0],channel[1],channel[2],channel[3])

print "Are all the setting consistent? ", all([diff == 0 for diff in channel_diff])
