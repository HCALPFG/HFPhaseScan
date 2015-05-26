
from Configuration import mapFile



class mapping(object):
	"""a class to read in emap txt file and create a mapping between ieta,iphi,depth to rbx,qie,rm"""
	def __init__(self,mapFileName):
		self._file = open(mapFileName)

		self._map = {}
		
		for line in self._file:
			if line[0]=="#" : continue
			fieldList = line.split()
			if fieldList[6] != "HF": continue
			ieta = int(fieldList[2])
			iphi = int(fieldList[3])
			depth = int(fieldList[5])
			rbx = fieldList[7]
			subDet = rbx[:3]
			qie = int(fieldList[13])
			rm = int(fieldList[9])
			self._map[(ieta,iphi,depth,subDet)] = (rbx,qie,rm)


	def __str__(self):
		return "\n".join([ "ieta: {0}, iphi: {1}, depth: {2}, det: {3} corresponds to: RBX: {4}, QIE: {5}, RM: {6}".format(*(coord1+coord2) ) for coord1,coord2 in self._map.iteritems()   ] )
			


if __name__ == "__main__":
	a = mapping(mapFile())
	print a
