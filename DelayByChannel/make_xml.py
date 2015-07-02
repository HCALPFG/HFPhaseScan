import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from DelaySetting import DelaySetting
from XMLProducer import XMLProducer


inputBrickPath = "/afs/cern.ch/work/k/klo/hcal/PromptAnalysis/HFPhaseScan/DelayByChannel/Data/20150521_HFPhaseScan_Shift0_Edmund/delay/"
inputTTCRXPath = "/afs/cern.ch/work/k/klo/hcal/PromptAnalysis/HFPhaseScan/DelayByChannel/Data/20150521_HFPhaseScan_Shift0_Edmund/ttcrx.xml"
mapPath = "Data/2015-may-4_HCALmapHBEF_G_uHTR.txt"

# relativeTimingPath = "/afs/cern.ch/work/k/klo/hcal/PromptAnalysis/HFPhaseScan/DelayByChannel/Data/20150608_HFRelativeTiming.txt"
relativeTimingPath = {"depth1":("Data/20150528_RelativeTimeShift.root","shift_depth1"),"depth2":("Data/20150528_RelativeTimeShift.root","shift_depth2")}
outputPath = "/afs/cern.ch/work/k/klo/hcal/PromptAnalysis/HFPhaseScan/DelayByChannel/output/HFPhaseScan_July01-2015_5050/"

delaySetting = DelaySetting(inputBrickPath,inputTTCRXPath,mapPath)
delaySetting.readDelayFromXML()
delaySetting.readDelayFromHisto(relativeTimingPath)
delaySetting.adjustTiming()
producer = XMLProducer()
producer.produce(delaySetting,"2015-july-01_HCAL_Delays","01-07-15","All30","ttcrx.xml",outputPath)
