import sys
sys.path.append("/usr/local/lib/python2.7/dist-packages")
from bs4 import BeautifulSoup as bs
import xml.etree.ElementTree as ET
import requests, re

def loadTreasuryCurve():
    ''' uses beautiful soup to scrape treasury xml for curve points'''
    url = 'http://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=month(NEW_DATE)%20eq%204%20and%20year(NEW_DATE)%20eq%202017'
    data = requests.get(url).text
    root = ET.fromstring(data)
    for child in root:
        print(child.tag, child.attrib)
    
    for entry in root.findall('entry'):
        print(entry.tag, entry.attrib)
    
    for entry in root.iter('entry'):
        print(entry.tag, entry.attrib)
    
    import pdb; pdb.set_trace()
    print()

if __name__ == "__main__":
    loadTreasuryCurve()
    # import pdb; pdb.set_trace()