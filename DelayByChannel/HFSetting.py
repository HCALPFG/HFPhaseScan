from copy import deepcopy

class HFSetting(object):
	def __init__(self,mapFileName):
		self._file = open(mapFileName)

		self._setting = {}
		self._map = {}
		self._RBXSetting = {}

		for line in self._file:
			if line[0] == "#": continue
			fieldList = line.split()
			if fieldList[6] != "HF": continue
			ieta = int(fieldList[2])
			iphi = int(fieldList[3])
			depth = int(fieldList[5])
			subDet = fieldList[7][:3]
			self._setting[(ieta,iphi,depth,subDet)] = ""
			rbx = fieldList[7]
			qie = int(fieldList[12])
			rm = int(fieldList[9])
			cand = int(fieldList[11])
			self._map[(ieta,iphi,depth,subDet)] = deepcopy((rbx,qie,rm,cand))
			self._RBXSetting[(rbx,qie,rm,cand)] = ""

	
	def setValue(self,value,ieta,iphi,depth,subDet):
		if (ieta,iphi,depth,subDet) in self._setting:
			self._setting[(ieta,iphi,depth,subDet)] = value
			self._RBXSetting[self.getRBXCoords(ieta,iphi,depth,subDet)] = value
		else:
			raise RuntimeError,"Can't find (ieta,iphi,depth,subDet) in the emap for HF"
	
	def __iter__(self):
		return iter(self._RBXSetting)

	def getValue(self,ieta,iphi,depth,subDet):
		return self._setting[(ieta,iphi,depth,subDet)]

	def cleanUp(self):
		self._file.close()

	def getRBXCoords(self,ieta,iphi,depth,subDet):
		if (ieta,iphi,depth,subDet) in self._map:
			return self._map[(ieta,iphi,depth,subDet)]
		else:
			raise RuntimeError,"Can't find (ieta,iphi,depth,subDet) in the emap for HF"

	def getRBXValue(self,coord):
		return self._RBXSetting[coord]
