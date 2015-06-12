from xml.dom import minidom

inputPath = "Data/20150521_HFPhaseScan_Shift0_Edmund/ttcrx.xml"
outputPath = "output/HFPhaseScan_June13-2015_5050/ttcrx.xml"
inFile = minidom.parse(inputPath)
outFile = minidom.parse(outputPath)

inData = inFile.getElementsByTagName("Data")
outData = outFile.getElementsByTagName("Data")

inSetting = {}
for k in inData:
	inSetting[str(k.getAttribute("id"))] = k.childNodes[0].nodeValue

outSetting = {}
for k in outData:
	outSetting[str(k.getAttribute("id"))] = k.childNodes[0].nodeValue


# inSetting = { str(k.getAttribute("id")):k.childNodes[0].nodeValue for k in inData }
# outSetting = { str(k.getAttribute("id")):k.childNodes[0].nodeValue for k in outData }

if len(inSetting) != len(outSetting):
	print "Number of RBX in the two ttcrx.xml are different"

changedRBX = []

for rbx,setting in inSetting.iteritems():
	print "====================="
	print "RBX: ",rbx
	print "inData: ", setting
	print "outData: ", outSetting[rbx]
	if setting != outSetting[rbx]:
		changedRBX.append(rbx)

for rbx in changedRBX:
	print "====================="
	print "Setting of RBX %s is changed as followed"%rbx
	print "in: ", inSetting[rbx]
	print "out: ", outSetting[rbx]



