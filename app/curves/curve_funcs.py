import sys
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import requests, re, time, datetime, pdb
import numpy as np
from app import app
from config import IMG_PATH
from bs4 import BeautifulSoup as bs
# import xml.etree.ElementTree as ET
from lxml import etree
from app.curves.curves import Curve


TSY_CURVE_MAP = {
    'BC_1MONTH' : 30,
    'BC_3MONTH' : 91,
    'BC_6MONTH' : 182,
    'BC_1YEAR' : 365,
    'BC_2YEAR' : 730,
    'BC_3YEAR' : 1095,
    'BC_5YEAR' : 1825,
    'BC_7YEAR' : 2555,
    'BC_10YEAR' : 3650,
    'BC_20YEAR' : 7300,
    'BC_30YEAR' : 10950,
}

def loadTreasuryCurve(dflt=False, disp=True):
    ''' uses beautiful soup to scrape treasury xml for curve points
    
    Parameters
    ==========
    dflt : bool
        when set to true, loads a default curve that has the right format
        but rates might be out of date
    disp : bool
        when true, will save the matplotlib image
    
    Return
    ======
    curve : Curve object
        a curve of treasury rates
    '''
    
    if dflt:
        rate_list = [[datetime.date(2017, 5, 30), 0.0068], [datetime.date(2017, 7, 30), 0.008], [datetime.date(2017, 10, 29), 0.0099],
                    [datetime.date(2018, 4, 30), 0.0107], [datetime.date(2019, 4, 30), 0.0128], [datetime.date(2020, 4, 29), 0.0145], 
                    [datetime.date(2022, 4, 29), 0.0181], [datetime.date(2024, 4, 28), 0.021], [datetime.date(2027, 4, 28), 0.0229], 
                    [datetime.date(2037, 4, 25), 0.0267], [datetime.date(2047, 4, 23), 0.0296]]
        if disp:
            saveCurveImg(rate_list)
        return Curve([r[0] for r in rate_list], [r[1] for r in rate_list])
    
    url = 'http://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=month(NEW_DATE)%20eq%204%20and%20year(NEW_DATE)%20eq%202017'
    data = requests.get(url).text
    import pdb; pdb.set_trace()
    xml = bytes(bytearray(data, encoding='utf-8'))
    root = etree.XML(xml)
    # time.sleep((0.5))
    # weird funky thing with the format, will try to solve later
    # xml adds an xmlns namespace thing that latches on to each elements
    ns = ["{"+n+"}" for n in list(root.nsmap.values())]
    most_rec_curve = root.findall(ns[0] + "entry")[-1].find(ns[0]+'content')
    most_rec_curve = most_rec_curve.find(ns[1]+'properties')
    el_list = most_rec_curve.getchildren()
    
    id = el_list.pop(0).text
    dt = el_list.pop(0).text
    rate_list = []
    for el in el_list:
        rate_list.append([el.tag.replace(ns[2],""), el.text])
    # remove double 30 yr in data
    rate_list.pop(-1)
    # divide by 100 to get it in decimal form
    today = datetime.date.today()
    rate_list = [[today + datetime.timedelta(days=TSY_CURVE_MAP[r[0]]), float(r[1])/100] for r in rate_list]
    
    if disp:
        saveCurveImg(rate_list)
        
    return Curve([r[0] for r in rate_list], [r[1] for r in rate_list])

def saveCurveImg(rate_list):
    x = [r[0] for r in rate_list]
    y = [r[1] for r in rate_list]
    plt.plot(x, y)
    plt.xlabel('Date')
    plt.ylabel('Rate')
    plt.tight_layout()
    plt.savefig(IMG_PATH + 'tsy_curve.png', dpi=300)

def flatInterp(mat_dt, crv):
    below = 0
    for i in crv._curve:
        if i[0] > mat_dt:
            above = i
            break
        else:
            below = i
            above = None
    if not above:
        return below
    if not below:
        return above
    if (abs(above[0] - mat_dt) < abs(below[0] - mat_dt)):
        return above
    else:
        return below

def linearInterp(mat_dt, crv):
    below = 0
    for i in crv._curve:
        if i[0] > mat_dt:
            above = i
            break
        else:
            below = i
            above = None
    if not above:
        return below
    if not below:
        # assume a bottom point of 0 and time of right now
        # Not a perfect assumption but its an edge case for the real short end
        below = (datetime.date.today(), 0)
    interp = ((mat_dt - below[0]) / (above[0] - below[0])) * (above[1] - below[1]) + below[1]
    return [mat_dt, interp]
    

if __name__ == "__main__":
    loadTreasuryCurve(dflt=True)