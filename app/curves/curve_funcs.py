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
from app.utils.fi_funcs import *


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
    ''' uses lxml / etree to scrape treasury xml for curve points
    
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
    # lw = line width, b = blue line, ro = red points
    plt.plot(x, y, 'b', lw=1.5)
    plt.plot(x, y, 'ro')
    plt.xlabel('Date')
    plt.ylabel('Rate')
    plt.axis('tight')
    plt.grid(True)
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

def convertSpotToParCurve(crv, trade_date=datetime.date.today(), par=100):
    """ Will bootstrap the spot rates given together to calculate the par rates. Using
    the previously calculated rate to discount for the next rate
    
    Parameters
    ==========
    crv : Curve object
        holds a list of maturity date and rate pairs in a tuple

    Return
    ======
    list of tuples representing the par curve
    """
    crv = crv._curve
    crv = [((c[0]-trade_date).days, c[1]) for c in crv]
    par_curve = []
    for i in range(len(crv)):
        if i == 0:
            par_curve.append(crv[i])
            continue
        
        par_crv_func = lambda y: \
            sum([y/(1+r)**(t/365) for t,r in crv[:i]]) + (y+par)/(1+crv[i][1])**(crv[i][0]/365)  - par
            # sum([y/(1+r)**(t/365) for t,r in crv[:i]].append((y+par)/(1+crv[i][1])**(crv[i][0]/365))) - par
        guess = crv[i][1]
        rate = newton_raphson(par_crv_func, guess)
        # par_curve.append((trade_date+datetime.timedelta(crv[i][0]),rate))
        par_curve.append((crv[i][0], rate/100))
    
    par_curve = [(trade_date + datetime.timedelta(crv[0]), crv[1]) for crv in par_curve]
    return par_curve
    
    
    return par_crv
    
def convertSpotToForwardCurve(crv):
    crv = crv._curve
    crv = [((c[0]-trade_date).days, c[1]) for c in crv]
    fwd_rates = []
    for i in len(crv):
        if i == 0:
            fwd_rates.append(i)
            continue
        # still working on this guy
        fr = ((1+crv[i][1])**(crv[i][0]/365)) / ((1+crv[i-1][1])**(crv[i][1]/365))**(1/B-A from equation in vitalsource)

if __name__ == "__main__":
    curve_temp = [(datetime.date(2018,5,7), 0.05263), (datetime.date(2019,5,7), 0.05616),
                (datetime.date(2020,5,7), 0.06359), (datetime.date(2021,5,7), 0.0700)]
    tsy_crv = Curve(rates=[r[1] for r in curve_temp], dts = [r[0] for r in curve_temp])
    convertSpotToParCurve(tsy_crv, datetime.date(2017,5,7))