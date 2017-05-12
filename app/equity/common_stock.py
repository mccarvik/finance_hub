import sys
import numpy as np
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import datetime, pdb
from app.equity.equity import Equity
from app.utils.fi_funcs import *
from app.curves.curve_funcs import *


class CommonStock(Equity):
    '''This class will represent an individual stock'''
    
    def __init__(self, div_yld=0.0, div_freq=0.25, cur_px=100, beta=1,
                trade_dt=datetime.date.today()):
        '''Constructor'''
        super().__init__(div_yld, div_freq, cur_px)
        self._trade_dt = trade_dt
        self._beta = beta
        
    def calcDividendDiscountModel(self, hold_per, sale_px, r_req=None, divs=False):
        ''' Calculates the value of the stock based on the Dividend
        Discount Model
        
        Parameters
        ==========
        r_req : float
            The required rate of return
            DEFAULT = Use the CAPM model and all its assumptions
        hold_per : float
            The holding period for the investment, expressed in years
        sale_px : float
            assumed price at sale of investment
        divs : list of floats
            the dividends if explicitly given
            
        Return
        ======
        pv : float
            The assumed present value based on DDM
        '''
        if not r_req:
            r_req = calcCAPM()
        
        if not divs:
            div_flows = np.array(createCashFlows(self._trade_dt, self._div_freq,
                        self._trade_dt + datetime.timedelta(365*hold_per),
                        self._div_yld, sale_px))
        else:
            div_flows = divs
        
        pv = 0
        p = 1
        for d in div_flows:
            pv += calcPV(d, r_req*self._div_freq, p)
            p += 1
        pv += calcPV(sale_px, r_req*self._div_freq, hold_per/self._div_freq)
        return pv 
    
    def calcCAPM(self, r_f=None, r_market=0.08):
        ''' Will calculate the Capital Asset Pricing Model require rate of return
            given the following parameter assumptions
            Model --> r = r_free + beta * (market risk premium)
        
        Parameters
        ==========
        r_f : float
            The risk free rate
            DEFAULT = 10 year treasury rate
        r_market : float
            Expected return on the market
            DEFAULT = 0.08, this is the historical number without adjusting for inflation
        
        Return
        ======
        capm r : float
            The CAPM calculated required rate of return
        '''
        if not r_f:
            r_f = linearInterp(self._trade_dt + datetime.timedelta(3650), loadTreasuryCurve(dflt=True, disp=False))[1]
        return r_f + self._beta * (r_market - r_f)
    
    def calcGordonGrowthModel(self, growth=None, r_f=None, D0=None):
        if not D0:
            D0 = self._cur_px * self._div_yld
        if not r_f:
            r_f = linearInterp(self._trade_dt + datetime.timedelta(3650), loadTreasuryCurve(dflt=True, disp=False))[1]
        if not growth:
            growth = calcGrowthEstimate()
        return (D0 * (1 + growth)) / (r_f - growth)
    
    def calcGrowthEstimage(self):
        b = (1 - div_payout_ratio)
        ROE = 1
        return (b * ROE)

if __name__ == "__main__":
    e = CommonStock(div_yld=0.02, div_freq=1, trade_dt=datetime.date(2017,1,1))
    divs = [2, 2.1, 2.2]
    # print(e.calcDividendDiscountModel(3, 20, 0.10, divs=divs))
    # print(e.calcCAPM())
    print(e.calcGordonGrowthModel(growth=0.14, r_f=0.19, D0=2.28))