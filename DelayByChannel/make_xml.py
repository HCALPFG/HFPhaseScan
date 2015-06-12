import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from DelaySetting import DelaySetting
from Configuration import delaySettingFiles,mapFile,brickDir,TTCPath
from XMLProducer import XMLProducer


delaySetting = DelaySetting(brickDir(),TTCPath(),mapFile())
delaySetting.readDelayFromXML()
delaySetting.readDelayFromHisto(delaySettingFiles())
delaySetting.adjustTiming()
producer = XMLProducer()
producer.produce(a,"2015-june-3_HCAL_Delays","03-06-15","All30","TTcrx_DELAY.xml","/afs/cern.ch/work/k/klo/hcal/PromptAnalysis/HFPhaseScan/HFPhaseScan_June03-2015/5050")
