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

def saveCurveImg(crv, trade_date=datetime.date.today()):
    ''' Will save a graph with spot (aka zero) rates, par rates, and forward rates
        Will calc the par rates and fwd rates from the spot rates
    
    Parameters
    ==========
    crv : Curve Object
        has a list of tuples holding maturity and spot rate pairs
        
    Return
    ======
    NONE
    '''
    pdb.set_trace()
    # x = [(r[0] - trade_date).days for r in crv._curve]
    x = [r[0] for r in crv._curve]
    y1 = [r[1] for r in crv._curve]                                     # spot rates
    y2 = [r[1] for r in convertSpotToParCurve(crv, trade_date)]         # par rates
    y3 = [r[2] for r in convertSpotToForwardCurve(crv, trade_date)]     # fwd rates
    
    # To anchor curve at 0
    x = [trade_date] + x
    y1 = [0] + y1
    y2 = [0] + y2
    y3 = [0] + y3
    
    # lw = line width, b = blue line, ro = red points
    plt.plot(x, y1, 'b', lw=1.5, label='SPOT')
    plt.plot(x, y1, 'ro')
    plt.plot(x, y2, 'g', lw=1.5, label='PAR')
    plt.plot(x, y2, 'ro')
    plt.plot(x, y3, 'k', lw=1.5, label='FWD')
    plt.plot(x, y3, 'ro')
    plt.legend(loc='upper left')
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
    trade_date : date
        the date from when the calculation is being made
    par : float
        the theoretical par value of the bond

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
        guess = crv[i][1]
        rate = newton_raphson(par_crv_func, guess)
        par_curve.append((crv[i][0], rate/100))
    
    par_curve = [(trade_date + datetime.timedelta(crv[0]), crv[1]) for crv in par_curve]
    return par_curve

def convertSpotsToForward(spot1, spot2, trade_date=datetime.date.today(), p=1):
    """ Takes two spot rates and calculates the implied forward rate between them
    
    Parameters
    ==========
    spot1, spot2 : tuple(date, float)
        maturity, rate tuple
    trade_date : date
        the date from when the calculation is being made
    p : float
        the periodicity of the bond --> aka how many times a year there is a theoretical coupon
        Ex: 2 = semiannual bond basis

    Return
    ======
    tuple
        tuple --> 3 components, first is the start date of the implied forward, next is the end date
        and 3rd is the rate
        Ex: today is 2017-01-01, a 2y1y imp fwd with a rate of 4.5% will be: 
        (2019-01-01, 2020-01-01, 0.045)
    """
    A = round((spot1[0]-trade_date).days * p/365, 4)
    B = round((spot2[0]-trade_date).days * p/365, 4)
    dem = (1+spot1[1] / p) 
    num = (1+spot2[1] / p)
    fr = ((num**B) / (dem**A))**(1/(B-A)) - 1
    
    # This gets it back annualized
    fr *= p
    return (spot1[0], spot2[0], fr)

def convertSpotToForwardCurve(crv, trade_date=datetime.date.today(), p=1):
    """ Will bootstrap use the spot rates to calculate the forward rates to get from one
        spot rate to another
    
    Parameters
    ==========
    crv : Curve object
        holds a list of maturity date and rate pairs in a tuple
    trade_date : date
        the date from when the calculation is being made
    p : float
        the periodicity of the bond --> aka how many times a year there is a theoretical coupon
        Ex: 2 = semiannual bond basis

    Return
    ======
    list of tuples representing the forward curve
    tuple --> 3 components, first is the start date of the implied forward, next is the end date
    and 3rd is the rate
    Ex: if today is 2017-01-01, a 2y1y imp fwd with a rate of 4.5% will be: (2019-01-01, 2020-01-01, 0.045)
    """
    crv = crv._curve
    fwd_rates = []
    for i in range(len(crv)):
        if i == 0:
            fwd_rates.append((trade_date, crv[i][0], crv[i][1]))
            continue
        fwd_rates.append((convertSpotsToForward(crv[i-1], crv[i], trade_date, 2)))
    return fwd_rates

if __name__ == "__main__":
    t_curve = [(datetime.date(2018,5,7), 0.05263), (datetime.date(2019,5,7), 0.05616),
                (datetime.date(2020,5,7), 0.06359), (datetime.date(2021,5,7), 0.0700)]
    # t_curve = [(datetime.date(2018,5,7), 0.02548), (datetime.date(2019,5,7), 0.02983), 
    #             (datetime.date(2020,5,7), 0.02891)]
    # tsy_crv = Curve(rates=[r[1] for r in t_curve], dts = [r[0] for r in t_curve])
    # convertSpotToParCurve(tsy_crv, datetime.date(2017,5,7))
    # convertSpotToForwardCurve(tsy_crv, datetime.date(2017,5,7))
    
    
    # saveCurveImg(loadTreasuryCurve(dflt=True, disp=False), trade_date=datetime.date(2017,5,7))