
from xml.dom import minidom
import os

# rbxDir = "output/HFPhaseScan_July01-2015_5050/delay/"
# ttcrxPath = "output/HFPhaseScan_July01-2015_5050/ttcrx.xml"
# outDirPath = "check/2015-July-01-DelaySetting.txt"

rbxDir = "Data/20150521_HFPhaseScan_Shift0_Edmund/delay/"
ttcrxPath = "Data/20150521_HFPhaseScan_Shift0_Edmund/ttcrx.xml"
outDirPath = "check/2015-May-21-DelaySetting.txt"


outFile = open(outDirPath,"w")

brick_in_paths = [ rbxDir + "/" + p for p in os.listdir(rbxDir) if os.path.isfile(os.path.join(rbxDir,p)) and p.endswith(".xml") and not p.startswith(".") ]

delaySetting = {}
xmlFiles = {}
for brickPath in brick_in_paths:
	rbxName = brickPath.split("/")[-1][:5]
	xmlFiles[rbxName] = minidom.parse(brickPath)
	data = xmlFiles[rbxName].getElementsByTagName("Data")
	for datum in data:
		delaySetting[ ( rbxName,int(datum.getAttribute("qie")),int(datum.getAttribute("rm")),int(datum.getAttribute("card"))  ) ] = int(datum.childNodes[0].nodeValue)

ttcrxSetting = {}
ttcrxFile = minidom.parse(ttcrxPath)
data = ttcrxFile.getElementsByTagName("Data")
for datum in data:
	ttcrxSetting[str(datum.getAttribute("id"))] = datum.childNodes[0].nodeValue


for i,channel in enumerate(sorted(delaySetting)):
	outFile.write("Line {0}".format(i) + " RBX: {0}, QIE: {1}, RM: {2}, Card: {3};".format(*channel)+" Delay: {0} ".format( delaySetting[channel] ) + " ttcrx: " + ttcrxSetting[channel[0]] + "\n" )


outFile.close()
