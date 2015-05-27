from Configuration import delaySettingFiles,mapFile
from HFSetting import HFSetting
import ROOT as r

class DelaySetting(HFSetting):
	"""a class to ead DelaySetting from TH2"""
	def __init__(self,mapFileName,fileDict):
		super(DelaySetting,self).__init__(mapFileName)

		self._files = {}
		self._hists = {}

		for depth,inputInfo in fileDict.iteritems():
			fileName = inputInfo[0]
			histName = inputInfo[1]
			depthNumber = int(depth[-1])
			self._files[depthNumber] = r.TFile(fileName,"READ")
			self._hists[depthNumber] = self._files[depthNumber].Get(histName)

		for coord in self._setting:
			self.setValue(self._hists[coord[2]].GetBinContent(self._hists[coord[2]].GetXaxis().FindBin(coord[0]) ,self._hists[coord[2]].GetYaxis().FindBin(coord[1]) ),*coord)


	def __str__(self):
		# print delay setting for each channel, each line for each channel
		return "\n".join(["ieta: %s, iphi: %s, depth: %s, det: %s, delay: %s"%(coords[0],coords[1],coords[2],coords[3],delay)+", RBX: {0}, QIE: {1}, RM: {2}, Cand: {3}".format(*self.getRBXCoords(*coords)) for coords,delay in self._setting.iteritems() ])

	def cleanUp(self):
		super(DelaySetting,self).cleanUp()
		for depth,file in self._files.iteritems():
			file.Close()
	
	def getDelay(self,ieta,iphi,depth,subDet):
		return self._setting[(ieta,iphi,depth,subDet)]



if __name__ == "__main__":
	a = DelaySetting(mapFile(),delaySettingFiles())
	print a
	a.cleanUp()

