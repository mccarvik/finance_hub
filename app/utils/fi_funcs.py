import datetime, sys
from scipy import optimize
from math import sqrt, pi, log, e
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# from pandas.io.data import DataReader


def bootstrap(first_zero_rate, first_mat, bs_rate_mats):
    """
    bs_rate_mats = list of tuples in the format (fwd_rate, maturity)
    """
    new_bs_rate_mats = []
    next_bs_zero_rate = ((bs_rate_mats[0][0] * bs_rate_mats[0][1]) + (first_zero_rate * first_mat)) / (bs_rate_mats[0][1] + first_mat)
    new_bs_rate_mats.append(tuple([bs_rate_mats[0][1] + first_mat, next_bs_zero_rate]))
    for i in range(len(bs_rate_mats)):
        if i == 0:
            continue
        
        next_bs_zero_rate = ((bs_rate_mats[i][0] * bs_rate_mats[i][1]) + \
            (new_bs_rate_mats[-1][1] * new_bs_rate_mats[-1][0])) / \
            (bs_rate_mats[i][1] + new_bs_rate_mats[-1][0])
        new_bs_rate_mats.append(tuple([bs_rate_mats[i][1] + new_bs_rate_mats[-1][0], next_bs_zero_rate]))
    return new_bs_rate_mats


def cumPresentValue(today, annual_disc_rate, cfs, freq=1, cont=True):
    cum_pv = 0
    # freq if rate passed in is not annual, ex: 0.5 = semiannual
    ir = annual_disc_rate * freq
    for i in cfs:
        period = ((i[0] - today).days / 365) / freq
        if cont:
            cum_pv += calcPVContinuous(i[1], ir, period)
        else:
            cum_pv += calcPV(i[1], ir, period)
    return cum_pv

def calcPV(cf, ir, period):
    return (cf / (1+ir)**period)

def calcPVContinuous(cf, ir, period):
    return cf * e**((-1) * ir * period)


def createCashFlows(start_date, freq, tenor, cpn, par):
    num_cfs = (1 / freq) * tenor
    days_from_issue = [int((365 * freq)*(i+1)) for i in range(int(num_cfs))]
    dates = [start_date + datetime.timedelta(i) for i in days_from_issue]
    cfs = [(dates[i], cpn * par * freq) for i in range(len(dates))]
    cfs[-1] = (cfs[-1][0], cfs[-1][-1] + par)
    return cfs

def calcYieldToDate(price, par, tenor, cpn, freq=0.5, guess=None, start_date=datetime.datetime.today()):
    freq = float(freq)
    # guess ytm = coupon rate, will get us in the ball park
    guess = cpn / par
    cfs = createCashFlows(start_date, freq, tenor, cpn, par)
    # convert cpn from annual rate to actual coupon
    coupon = cpn * freq
    dts = [(i[0] - datetime.datetime.today()).days / 365 for i in cfs]
    ytm_func = lambda y: \
        sum([coupon/(1+y*freq)**(t/freq) for t in dts]) + \
        par/(1+y*freq)**(tenor/freq) - price
        
    # return optimize.newton(ytm_func, guess)
    return newton_raphson(ytm_func, guess)

def derivative(f, x, h):
      return (f(x+h) - f(x-h)) / (2.0*h)  # might want to return a small non-zero if ==0

def newton_raphson(func, guess, rng=0.0001):
    lastX = guess
    nextX = lastX + 10* rng  # "different than lastX so loop starts OK
    while (abs(lastX - nextX) > rng):  # this is how you terminate the loop - note use of abs()
        newY = func(nextX)                     # just for debug... see what happens
        print("f(", nextX, ") = ", newY)     # print out progress... again just debug
        lastX = nextX
        nextX = lastX - newY / derivative(func, lastX, rng)  # update estimate using N-R
    return nextX
    
def calcSurvivalRate(time, rate):
    # time measured in years
    return (e**(-1*time*rate))

def VaR(symbol='AAPL', notl=None, conf=0.95, dist=None, _d1=None, _d2=None, volwindow=50, varwindow=250):
    # Retrieve the data from Internet
    # Choose a time period
    d1 = _d1 if _d1 else datetime.datetime(2001, 1, 1)
    d2 = _d2 if _d2 else datetime.datetime(2012, 1, 1)
    #get the tickers
    price = DataReader(symbol, "yahoo",d1,d2)['Adj Close']
    price = price.asfreq('B').fillna(method='pad')
    ret = price.pct_change()
    
    #choose the quantile
    quantile=1-conf
    
    import pdb; pdb.set_trace()
    #simple VaR using all the data
    # VaR on average accross all the data
    unnormedquantile=pd.expanding_quantile(ret,quantile)
    
    # similar one using a rolling window 
    # VaR only calculated over the varwindow, rolling
    unnormedquantileR=pd.rolling_quantile(ret,varwindow,quantile)
    
    #we can also normalize the returns by the vol
    vol=pd.rolling_std(ret,volwindow)*np.sqrt(256)
    unitvol=ret/vol
    
    #and get the expanding or rolling quantiles
    # Same calcs as above except normalized so show VaR in
    # standard deviations instead of expected returns
    Var=pd.expanding_quantile(unitvol,quantile)
    VarR=pd.rolling_quantile(unitvol,varwindow,quantile)
    
    normedquantile=Var*vol
    normedquantileR=VarR*vol
    
    ret2=ret.shift(-1)
    courbe=pd.DataFrame({'returns':ret2,
                  'quantiles':unnormedquantile,
                  'Rolling quantiles':unnormedquantileR,
                  'Normed quantiles':normedquantile,
                  'Rolling Normed quantiles':normedquantileR,
                  })
    
    courbe['nqBreak']=np.sign(ret2-normedquantile)/(-2) +0.5
    courbe['nqBreakR']=np.sign(ret2-normedquantileR)/(-2) +0.5
    courbe['UnqBreak']=np.sign(ret2-unnormedquantile)/(-2) +0.5
    courbe['UnqBreakR']=np.sign(ret2-unnormedquantileR)/(-2) +0.5
    
    nbdays=price.count()
    print('Number of returns worse than the VaR')
    print('Ideal Var                : ', (quantile)*nbdays)
    print('Simple VaR               : ', np.sum(courbe['UnqBreak']))
    print('Normalized VaR           : ', np.sum(courbe['nqBreak']))
    print('---------------------------')
    print('Ideal Rolling Var        : ', (quantile)*(nbdays-varwindow))
    print('Rolling VaR              : ', np.sum(courbe['UnqBreakR']))
    print('Rolling Normalized VaR   : ', np.sum(courbe['nqBreakR']))
    
    
if __name__ == "__main__":
    # import pdb; pdb.set_trace()
    pass
    # print(bootstrap(0.048, 400, [(0.053, 91), (0.055, 98)]))
    # print(calcYieldToDate(95.0428, 100, 1.5, 5.75))
    # print(calcYieldToDate(100, 100, 2, 6))
    # xFound = newton_raphson(quadratic, 5, 0.01)    # call the solver
    # print("solution: x = ", xFound)
    VaR()