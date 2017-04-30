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
    # weird funky thing with the format, will try to solve later
    # xml adds an xmlns namespace thing that latches on to each elements
    ns = ["{"+n+"}" for n in list(root.nsmap.values())]
    most_rec_curve = root.findall(ns[0] + "entry")[-1].find(ns[0]+'content')
    most_rec_curve = most_rec_curve.find(ns[1]+'properties')
    el_list = most_rec_curve.getchildren()
    
    id = el_list.pop(0).text
    dt = el_list.pop(0).text
    import pdb; pdb.set_trace()
    rate_list = []
    for el in el_list:
        rate_list.append([el.tag.replace(ns[2],""), el.text])
    
    import pdb; pdb.set_trace()
    print()

if __name__ == "__main__":
    loadTreasuryCurve()
    # import pdb; pdb.set_trace()