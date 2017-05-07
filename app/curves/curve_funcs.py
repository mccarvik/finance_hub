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
        rate_list = readCurve('tsy')
        if disp:
            saveCurveImg(rate_list)
        return Curve([r[0] for r in rate_list], [r[1] for r in rate_list])
    
    url = 'http://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=month(NEW_DATE)%20eq%204%20and%20year(NEW_DATE)%20eq%202017'
    
    # time.sleep((0.5))
    # weird funky thing with the format, will try to solve later
    # xml adds an xmlns namespace thing that latches on to each elements
    el_list = None
    data = requests.get(url).text
    xml = bytes(bytearray(data, encoding='utf-8'))
    root = etree.XML(xml)
    ns = ["{"+n+"}" for n in list(root.nsmap.values())]
    for j in range(len(ns)):
        try:
            most_rec_curve = root.findall(ns[j] + "entry")[-1].find(ns[j]+'content')
            for k in range(len(ns)):
                try:
                    most_rec_curve_t = most_rec_curve.find(ns[k]+'properties')
                    el_list = most_rec_curve_t.getchildren()
                    if el_list:
                        break
                except:
                    print("not " + ns[k])
            if el_list:
                break
        except:
            print("not " + ns[j])
        
    
    if not el_list:
        raise "XML ERROR"
    
    id = el_list.pop(0).text
    dt = el_list.pop(0).text
    rate_list = []
    for el in el_list:
        for n in ns:
            el.tag = el.tag.replace(n,"")
        rate_list.append([el.tag, el.text])
    # remove double 30 yr in data
    rate_list.pop(-1)
    # divide by 100 to get it in decimal form
    today = datetime.date.today()
    rate_list = [[today + datetime.timedelta(days=TSY_CURVE_MAP[r[0]]), float(r[1])/100] for r in rate_list]
    
    if disp:
        saveCurveImg(rate_list)
    
    crv = Curve([r[0] for r in rate_list], [r[1] for r in rate_list])
    saveCurve(crv, "tsy")
    return crv

def saveCurveImg(rate_list):
    x = [r[0] for r in rate_list]
    y = [r[1] for r in rate_list]
    plt.plot(x, y)
    plt.xlabel('Date')
    plt.ylabel('Rate')
    plt.tight_layout()
    plt.savefig(IMG_PATH + 'tsy_curve.png', dpi=300)

def saveCurve(curve, crv_str):
    today = datetime.date.today()
    file_name = crv_str + "_recent.csv"
    file_path = "/home/ubuntu/workspace/finance/app/curves/curve_files/"
    
    with open(file_path + file_name, 'w') as file:
        file.write(crv_str + ", " + today.strftime('%Y%m%d') + "\n")
        for i in curve._curve:
            file.write(str((i[0] - today).days) + ", " + str(i[1]) + "\n")

def readCurve(crv_str):
    file_name = crv_str + "_recent.csv"
    file_path = "/home/ubuntu/workspace/finance/app/curves/curve_files/"
    with open(file_path + file_name, 'r') as file:
        content = file.readlines()
        content = content[1:]
        rate_list = []
        today = datetime.date.today()
        for c in content:
            data = c.split(",")
            rate_list.append([today + datetime.timedelta(float(data[0])), float(data[1])])
    return rate_list

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

def convertSpotToParCurve(crv):
    pass

if __name__ == "__main__":
    loadTreasuryCurve(dflt=True)