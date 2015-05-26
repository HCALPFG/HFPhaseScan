from Configuration import delaySettingFiles
import ROOT as r


class DelaySetting(object):
	"""a class to ead DelaySetting from TH2"""
	def __init__(self,fileDict):
		self._files = {}
		self._hists = {}

		for depth,inputInfo in fileDict.iteritems():
			fileName = inputInfo[0]
			histName = inputInfo[1]
			depthNumber = int(depth[-1])
			self._files[depthNumber] = r.TFile(fileName,"READ")
			self._hists[depthNumber] = self._files[depthNumber].Get(histName)

		self._setting = {}
		for depth,hist in self._hists.iteritems():
			for ietaBin in range(hist.GetXaxis().GetNbins()):
				for iphiBin in range(hist.GetYaxis().GetNbins()):
					ieta = int(hist.GetXaxis().GetBinCenter(ietaBin))
					iphi = int(hist.GetYaxis().GetBinCenter(iphiBin))
					self._setting[(ieta,iphi,depth)] = hist.GetBinContent(ietaBin,iphiBin)
	
	def __str__(self):
		# print delay setting for each channel, each line for each channel
		return "\n".join(["ieta: %s, iphi: %s, depth: %s, delay: %s"%(coords[0],coords[1],coords[2],delay) for coords,delay in self._setting.iteritems() ])

	def cleanUp(self):
		for depth,file in self._files.iteritems():
			file.Close()
	
	def getDelay(self,ieta,iphi,depth):
		return self._setting[(ieta,iphi,depth)]



if __name__ == "__main__":
	a = DelaySetting(delaySettingFiles())
	print a
	a.cleanUp()

