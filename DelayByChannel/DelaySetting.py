from Configuration import delaySettingFiles,mapFile,brickDir,TTCPath
from HFSetting import HFSetting
import ROOT as r
import os
from xml.dom import minidom

class DelaySetting(HFSetting):
	"""a class to read DelaySetting from TH2 and XML"""
	def __init__(self,rbxDir,TTCrxFilePath,mapFileName):
		super(DelaySetting,self).__init__(mapFileName)
		self.rbxDir = rbxDir
		self.ttcrxPath = TTCrxFilePath
		self.brick_in_paths = [ rbxDir + "/" + p for p in os.listdir(rbxDir) if os.path.isfile(os.path.join(rbxDir,p)) and p.endswith(".xml") ]
		
		# Default Setting
		self.HF_CalibRM_number = 4
		self.brick_min_delay = 0
		self.brick_max_delay = 24
		self.brick_width = 25
		self.ttcrx_min_delay = 0
		self.ttcrx_max_delay = 225
		self.ttcrx_step_time_ns = 15

	def readDelayFromXML(self):
		self._hcalRBXSetting = {}
		self._hcalChSetting = {}
		self._xmlFiles = {}

		for brickPath in self.brick_in_paths:
			rbxName = brickPath.split("/")[-1][:5]
			self._xmlFiles[rbxName] = minidom.parse(brickPath)
			data = self._xmlFiles[rbxName].getElementsByTagName("Data")
			for datum in data:
				self._hcalChSetting[ ( rbxName,int(datum.getAttribute("qie")),int(datum.getAttribute("rm")),int(datum.getAttribute("card"))  ) ] = int(datum.childNodes[0].nodeValue)

		ttcrxFile = minidom.parse(self.ttcrxPath)
		ttcrxData = ttcrxFile.getElementsByTagName("Data")
		for datum in ttcrxData:
			if "HF" not in datum.getAttribute("id"): continue
			self._hcalRBXSetting[str(datum.getAttribute("id"))] = int(datum.childNodes[0].nodeValue.split(" ")[0])


	def readDelayFromHisto(self,fileDict):
		self._files = {}
		self._hists = {}
		self._relSetting = {}

		for depth,inputInfo in fileDict.iteritems():
			fileName = inputInfo[0]
			histName = inputInfo[1]
			depthNumber = int(depth[-1])
			self._files[depthNumber] = r.TFile(fileName,"READ")
			self._hists[depthNumber] = self._files[depthNumber].Get(histName)

		for coord in self._EtaPhiSetting:
			delay = self._hists[coord[2]].GetBinContent(self._hists[coord[2]].GetXaxis().FindBin(coord[0]) ,self._hists[coord[2]].GetYaxis().FindBin(coord[1]) )
			self._relSetting[self.getRBXCoords(*coord)] = int(delay)

	def adjustTiming(self):
		if hasattr(self,"_hcalRBXSetting") and hasattr(self,"_hcalChSetting") and hasattr(self,"_relSetting"):
			successShift = False
			self._adjustChSetting = {}
			self._adjustRBXSetting = {}
			# Loop over each RBX
			for rbxName,RBXDelay in self._hcalRBXSetting.iteritems():
				self._goodChannels = {(coord[1],coord[2],coord[3]):True for coord in self._hcalChSetting if coord[0] == rbxName}
				self._delayOneChannel = {(coord[1],coord[2],coord[3]):delay for coord,delay in self._hcalChSetting.iteritems() if coord[0] == rbxName}

				# Loop over each channel and check if there is out of bound
				for channelCoord,currentDelay in self._delayOneChannel.iteritems():
					if channelCoord[1] == self.HF_CalibRM_number: continue	
					if (self._relSetting[(rbxName,channelCoord[0],channelCoord[1],channelCoord[2])] + currentDelay > self.brick_max_delay) or  (self._relSetting[(rbxName,channelCoord[0],channelCoord[1],channelCoord[2])] + currentDelay < self.brick_min_delay):  		
					 	self._goodChannels[channelCoord] = False

				# Adjust timing according to if there is out of bound
				if False in self._goodChannels.values():
					listBadChannels = []
					print "Interplay with TTCrx..."
					print "List of bad channels:"
					print "=============================="
					for channelCoord,isGood in self._goodChannels.iteritems():
						if not isGood:
							print "RBX: {0}, QIE: {1}, RM: {2}, Card: {3};".format(rbxName,*channelCoord)+" Current Delay: {0}, Request Delay: {1}".format(self._delayOneChannel[channelCoord],self._relSetting[(rbxName,channelCoord[0],channelCoord[1],channelCoord[2])] )
							listBadChannels.append(channelCoord)


				
					for badChannel in listBadChannels:
						if successShift: continue
						requiredShift = self._relSetting[(rbxName,badChannel[0],badChannel[1],badChannel[2])] + self._delayOneChannel[badChannel]
						if requiredShift > 0:
							delay_for_ttcrx_ns = requiredShift - self.brick_max_delay
						else:
							delay_for_ttcrx_ns = requiredShift - self.brick_min_delay
						delay_for_ttcrx_nk = int(round(float(delay_for_ttcrx_ns) / self.ttcrx_step_time_ns) - .5) + (float(delay_for_ttcrx_ns) / self.ttcrx_step_time_ns > 0)
						delay_for_ttcrx_k = delay_for_ttcrx_k*self.ttcrx_step_time_ns
	
						# Check if this delay for ttcrx is compatible with the rest
						testAdjust = {goodChannel: self._delayOneChannel[goodChannel]-delay_for_ttcrx_ns + self._relSetting[(rbxName,goodChannel[0],goodChannel[1],goodChannel[2])]   for goodChannel,isGood in self._goodChannels.iteritems() if isGood }
						successShift = all([(adjustShiftWithTTcrx >= self.brick_min_delay) and (adjustShiftWithTTcrx <= self.brick_max_delay) for goodChannel,adjustShiftWithTTcrx in testAdjust.iteritems()  ])
						if successShift:
							for coord,currentDelay in self._delayOneChannel.iteritems():
								if coord[1] != 4:
									self._adjustChSetting[(rbxName,coord[0],coord[1],coord[2])] = currentDelay+self._relSetting[(rbxName,coord[0],coord[1],coord[2])]-delay_for_ttcrx_ns
								else:
									self._adjustChSetting[(rbxName,coord[0],coord[1],coord[2])] = 0
							self._adjustRBXSetting[rbxName] = delay_for_ttcrx_k
					
				else:
					for coord,currentDelay in self._delayOneChannel.iteritems():
						if coord[1] != self.HF_CalibRM_number:
							self._adjustChSetting[(rbxName,coord[0],coord[1],coord[2])] = currentDelay+self._relSetting[(rbxName,coord[0],coord[1],coord[2])]
						else:
							self._adjustChSetting[(rbxName,coord[0],coord[1],coord[2])] = 0
					self._adjustRBXSetting[rbxName] = self._hcalRBXSetting[rbxName]
					successShift = True

				if not successShift:
					print "WARNING! Illegal delays have been requested!"



		else:
			raise RuntimeError,"Delay Setting for RBX, channel or relative change not set"
	
	
	def adjustSetting(self):
		return self._adjustChSetting,self._adjustRBXSetting



	def __str__(self):
		# print delay setting for each channel, each line for each channel
		return "\n".join(["ieta: %s, iphi: %s, depth: %s, det: %s, delay: %s"%(coords[0],coords[1],coords[2],coords[3],delay)+", RBX: {0}, QIE: {1}, RM: {2}, Cand: {3}".format(*self.getRBXCoords(*coords)) for coords,delay in self._EtaPhiSetting.iteritems() ])

	def cleanUp(self):
		super(DelaySetting,self).cleanUp()
		for depth,file in self._files.iteritems():
			file.Close()

	


if __name__ == "__main__":
	a = DelaySetting(brickDir(),TTCPath(),mapFile())
	a.readDelayFromXML()
	a.readDelayFromHisto(delaySettingFiles())
	a.adjustTiming()
	# a.cleanUp()

