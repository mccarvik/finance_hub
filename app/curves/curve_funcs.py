import sys
sys.path.append("/usr/local/lib/python2.7/dist-packages")
from bs4 import BeautifulSoup as bs
# import xml.etree.ElementTree as ET
from lxml import etree
import requests, re

def loadTreasuryCurve():
    ''' uses beautiful soup to scrape treasury xml for curve points'''
    url = 'http://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=month(NEW_DATE)%20eq%204%20and%20year(NEW_DATE)%20eq%202017'
    data = requests.get(url).text
    xml = bytes(bytearray(data, encoding='utf-8')) 
    root = etree.XML(xml)
    ns = "{" + root.xpath('namespace-uri(.)') + "}"
    most_recent_curve = root.findall(ns + "entry")[-1].find(ns+'content')
    # weird funky thing with the format, will try to solve later
    # xml adds an xmlns namespace thing that latches on to each element
    
    import pdb; pdb.set_trace()
    print()

if __name__ == "__main__":
    loadTreasuryCurve()
    # import pdb; pdb.set_trace()