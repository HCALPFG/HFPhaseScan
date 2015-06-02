import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from DelaySetting import DelaySetting
from Configuration import delaySettingFiles,mapFile,brickDir,TTCPath


delaySetting = DelaySetting(brickDir(),TTCPath(),mapFile())
delaySetting.readDelayFromXML()
delaySetting.readDelayFromHisto(delaySettingFiles())
delaySetting.adjustTiming()
producer = XMLProducer()
producer.produce(a,"2015-june-1_HCAL_Delays","01-06-15","All30","TTcrx_DELAY.xml","/nfshome0/klo/HFPhaseScan/HFPhaseScan_June03-2015/5050/")
