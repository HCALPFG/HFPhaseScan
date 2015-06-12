from copy import deepcopy

class HFSetting(object):
	def __init__(self,mapFileName):
		self._file = open(mapFileName)

		self.channel_EtaPhiCoord = {}
		self.map = {}
		self.channel_RBXCoord = {}

		for line in self._file:
			if line[0] == "#": continue
			fieldList = line.split()
			if fieldList[6] != "HF": continue
			ieta = int(fieldList[2])
			iphi = int(fieldList[3])
			depth = int(fieldList[5])
			subDet = fieldList[7][:3]
			self.channel_EtaPhiCoord[(ieta,iphi,depth,subDet)] = ""
			rbx = fieldList[7]
			qie = int(fieldList[12])
			rm = int(fieldList[9])
			cand = int(fieldList[11])
			self.map[(ieta,iphi,depth,subDet)] = (rbx,qie,rm,cand)
			self.channel_RBXCoord[(rbx,qie,rm,cand)] = ""

	def __iter__(self):
		return iter(self.channel_RBXCoord)

	def cleanUp(self):
		self._file.close()

	def getRBXCoords(self,ieta,iphi,depth,subDet):
		if (ieta,iphi,depth,subDet) in self.map:
			return self.map[(ieta,iphi,depth,subDet)]
		else:
			raise RuntimeError,"Can't find (ieta,iphi,depth,subDet) in the emap for HF"

