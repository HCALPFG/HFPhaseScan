import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from DelaySetting import DelaySetting
from XMLProducer import XMLProducer


inputBrickPath = "/afs/cern.ch/work/k/klo/hcal/PromptAnalysis/HFPhaseScan/DelayByChannel/Data/DelaySetting_12July2015_5050/delay/"
inputTTCRXPath = "/afs/cern.ch/work/k/klo/hcal/PromptAnalysis/HFPhaseScan/DelayByChannel/Data/DelaySetting_12July2015_5050/ttcrx.xml"
mapPath = "Data/2015-may-4_HCALmapHBEF_G_uHTR.txt"
adjustFile = "/afs/cern.ch/work/k/klo/hcal/PromptAnalysis/HFPhaseScan/DelayByChannel/Data/AdjustSetting_14072015.txt"

# relativeTimingPath = "/afs/cern.ch/work/k/klo/hcal/PromptAnalysis/HFPhaseScan/DelayByChannel/Data/20150608_HFRelativeTiming.txt"
# relativeTimingPath = {"depth1":("Data/20150528_RelativeTimeShift.root","shift_depth1"),"depth2":("Data/20150528_RelativeTimeShift.root","shift_depth2")}
outputPath = "/afs/cern.ch/work/k/klo/hcal/PromptAnalysis/HFPhaseScan/DelayByChannel/output/DelaySetting_14July2015_5050/"

delaySetting = DelaySetting(inputBrickPath,inputTTCRXPath,mapPath)
delaySetting.readDelayFromXML()
delaySetting.readDelayFromTXT(adjustFile)
delaySetting.adjustTiming()
producer = XMLProducer()
producer.produce(delaySetting,"2015-july-14_HCAL_Delays","14-07-15","All30","ttcrx.xml",outputPath)
