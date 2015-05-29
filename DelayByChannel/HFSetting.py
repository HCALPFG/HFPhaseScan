from copy import deepcopy

class HFSetting(object):
	def __init__(self,mapFileName):
		self._file = open(mapFileName)

		self._EtaPhiSetting = {}
		self._map = {}
		self._RBXSetting = {}
		self._chSetting = {}

		for line in self._file:
			if line[0] == "#": continue
			fieldList = line.split()
			if fieldList[6] != "HF": continue
			ieta = int(fieldList[2])
			iphi = int(fieldList[3])
			depth = int(fieldList[5])
			subDet = fieldList[7][:3]
			self._EtaPhiSetting[(ieta,iphi,depth,subDet)] = ""
			rbx = fieldList[7]
			qie = int(fieldList[12])
			rm = int(fieldList[9])
			cand = int(fieldList[11])
			self._map[(ieta,iphi,depth,subDet)] = (rbx,qie,rm,cand)
			self._RBXSetting[rbx] = ""
			self._chSetting[(rbx,qie,rm,cand)] = ""

	
	def setValueWithEtaPhi(self,value,ieta,iphi,depth,subDet):
		if (ieta,iphi,depth,subDet) in self._EtaPhiSetting:
			self._setting[(ieta,iphi,depth,subDet)] = value
		else:
			raise RuntimeError,"Can't find (ieta,iphi,depth,subDet) in the emap for HF"
	
	def setValueWithCH(self,value,rbx,qie,rm,cand):
		if (rbx,qie,rm,cand) in self._chSetting:
			self._chSetting[(rbx,qie,rm,cand)] = value
		else:
			raise RuntimError,"Can't find (rbx,qie,rm,cand) in the emap for HF"

	def setValueWithRBX(self,value,rbx):
		if rbx in self._RBXSetting:
			self._RBXSetting[rbx] = value
		else:
			raise RuntimeError,"Can't find RBX in the emap for HF"
	
	def __iter__(self):
		return iter(self._chSetting)

	def cleanUp(self):
		self._file.close()

	def getRBXCoords(self,ieta,iphi,depth,subDet):
		if (ieta,iphi,depth,subDet) in self._map:
			return self._map[(ieta,iphi,depth,subDet)]
		else:
			raise RuntimeError,"Can't find (ieta,iphi,depth,subDet) in the emap for HF"

	def getRBXValue(self,coord):
		return self._chSetting[coord]
	
	def getChDelaySetting(self):
		return self._chSetting

	def getRBXDelaySetting(self):
		return self._RBXSetting
