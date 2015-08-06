from xml.dom import minidom
import os
import ROOT as r

class compareSetting(object):
	def __init__(self,inputBrickPath,outputBrickPath,mapPath,rootPaths):


		self.inBrick_in_paths = [ inputBrickPath + "/" + p for p in os.listdir(inputBrickPath) if os.path.isfile(os.path.join(inputBrickPath,p)) and p.endswith(".xml") and not p.startswith(".") ]
		self.inChSetting = {}
		self.inxmlFiles = {}
		for brickPath in self.inBrick_in_paths:
			rbxName = brickPath.split("/")[-1][:5]
			self.inChSetting[rbxName] = {}
			self.inxmlFiles[rbxName] = minidom.parse(brickPath)
			data = self.inxmlFiles[rbxName].getElementsByTagName("Data")
			for datum in data:
				self.inChSetting[rbxName][ (int(datum.getAttribute("qie")),int(datum.getAttribute("rm")),int(datum.getAttribute("card"))  ) ] = int(datum.childNodes[0].nodeValue)	



		self.outBrick_in_paths = [ outputBrickPath + "/" + p for p in os.listdir(outputBrickPath) if os.path.isfile(os.path.join(outputBrickPath,p)) and p.endswith(".xml") and not p.startswith(".") ]	
		self.outChSetting = {}
		self.outxmlFiles = {}
		for brickPath in self.outBrick_in_paths:
			rbxName = brickPath.split("/")[-1][:5]
			self.outChSetting[rbxName] = {}
			self.outxmlFiles[rbxName] = minidom.parse(brickPath)
			data = self.outxmlFiles[rbxName].getElementsByTagName("Data")
			for datum in data:
				self.outChSetting[rbxName][ ( int(datum.getAttribute("qie")),int(datum.getAttribute("rm")),int(datum.getAttribute("card"))  ) ] = int(datum.childNodes[0].nodeValue)	



		self.mapFile = open(mapPath)
		self.map = {}
		for line in self.mapFile:
			if line[0] == "#": continue
			fieldList = line.split()
			if fieldList[6] != "HF": continue
			ieta = int(fieldList[2])
			iphi = int(fieldList[3])
			depth = int(fieldList[5])
			subDet = fieldList[7][:3]
			rbx = fieldList[7]
			qie = int(fieldList[12])
			rm = int(fieldList[9])
			cand = int(fieldList[11])
			self.map[(ieta,iphi,depth,subDet)] = (rbx,qie,rm,cand)
		
		self.rootfiles = {}
		self.hists = {}
		for depth,inputInfo in rootPaths.iteritems():
			fileName = inputInfo[0]
			histName = inputInfo[1]
			depthNumber = int(depth[-1])
			self.rootfiles[depthNumber] = r.TFile(fileName,"READ")
			self.hists[depthNumber] = self.rootfiles[depthNumber].Get(histName)

		
		self.addSetting = {}
		for coord in self.map:
			delay = self.hists[coord[2]].GetBinContent(self.hists[coord[2]].GetXaxis().FindBin(coord[0]) ,self.hists[coord[2]].GetYaxis().FindBin(coord[1]) )

			rbxCoord = self.map[(coord[0],coord[1],coord[2],coord[3])]
			if rbxCoord[0] not in self.addSetting:
				self.addSetting[rbxCoord[0]] = {}
			self.addSetting[rbxCoord[0]][(rbxCoord[1],rbxCoord[2],rbxCoord[3])] = int(delay)

		self.rbxs = [ k  for k in self.addSetting ]


	def printRBXInfo(self,rbxName):
		badChannel = []
		for channel,inDelay in self.inChSetting[rbxName].iteritems():
			print "=================="
			print "channel: ", channel
			print "inDelay: ", inDelay
			print "outDelay: ", self.outChSetting[rbxName][channel]
			print "adjust: ",self.addSetting[rbxName][channel] if channel[1] != 4 else 0
			if channel[1] != 4:
				if inDelay+self.addSetting[rbxName][channel] != self.outChSetting[rbxName][channel]:
					badChannel.append(channel)
		for channel in badChannel:
			print "The channel", channel,"delay not consistent: "
			print "inDelay: ", inDelay
			print "outDelay: ", self.outChSetting[rbxName][channel]
			print "adjust: ",self.addSetting[rbxName][channel] if channel[1] != 4 else 0
		if len(self.inChSetting) != len(self.outChSetting):
			print "Number of input channel is not equal to the number of output channel"


inputBrickPath = "/afs/cern.ch/work/k/klo/hcal/PromptAnalysis/HFPhaseScan/DelayByChannel/Data/20150521_HFPhaseScan_Shift0_Edmund/delay/"
outputBrickPath = "/afs/cern.ch/work/k/klo/hcal/PromptAnalysis/HFPhaseScan/DelayByChannel/output/HFPhaseScan_June13-2015_5050/delay/"
mapPath = "Data/2015-may-4_HCALmapHBEF_G_uHTR.txt"

relativeTimingPath = {"depth1":("Data/20150528_RelativeTimeShift.root","shift_depth1"),"depth2":("Data/20150528_RelativeTimeShift.root","shift_depth2")}


compare = compareSetting(inputBrickPath,outputBrickPath,mapPath,relativeTimingPath)
compare.printRBXInfo("HFM04")
