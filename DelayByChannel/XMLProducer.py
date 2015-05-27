import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from DelaySetting import DelaySetting
from Configuration import delaySettingFiles,mapFile

class XMLProducer(object):
	def __init__(self):
		self.xmlData = {}

	def produce(self,delaySetting,creationTag,creationStamp,outDirPath):
		if not os.path.isdir(outDirPath):
			os.mkdir(outDirPath,0755)

		for channel in delaySetting:
			if channel[0] not in self.xmlData:
				self.xmlData[channel[0]] = []
			self.xmlData[channel[0]].append((channel[1],channel[2],channel[3],delaySetting.getRBXValue(channel)))

		for RBX,channelData in self.xmlData.iteritems():
			brick = ET.Element("CFGBrick")
			ET.SubElement(brick,"Parameter",name="RBX",type="string").text = RBX
			ET.SubElement(brick,"Parameter",name="INFOTYPE",type="string").text = "DELAY"
			ET.SubElement(brick,"Parameter",name="CREATIONTAG",type="string").text = creationTag
			ET.SubElement(brick,"Parameter",name="CREATIONSTAMP",type="string").text=creationStamp
			for channelDatum in channelData:
				ET.SubElement(brick,"Data",elements="1",encoding="dec",rm=str(channelDatum[1]),card=str(channelDatum[2]),qie=str(channelDatum[0])).text = str(int(channelDatum[3]))
			tree = ET.ElementTree(brick)
			xmlFile = open(outDirPath+RBX+"_DELAY.xml","w")
			xmlFile.write(minidom.parseString(ET.tostring(brick)).toprettyxml())
			xmlFile.close()





if __name__ == "__main__":
	a = DelaySetting(mapFile(),delaySettingFiles())
	test = XMLProducer()
	test.produce(a,"2015-may-27_HCAL_Delays_Test","09-02-14","/afs/cern.ch/work/k/klo/hcal/PromptAnalysis/HFPhaseScan/DelayByChannel/test/")

		



