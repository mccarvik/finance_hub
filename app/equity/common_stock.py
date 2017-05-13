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
        divs : list of lists of floats
            the dividend / date pairs if explicitly given
            
        Return
        ======
        pv : float
            The assumed present value based on DDM
        '''
        if not r_req:
            r_req = calcCAPM()
        
        if not divs:
            div_flows = createCashFlows(self._trade_dt, self._div_freq,
                        self._trade_dt + datetime.timedelta(365*hold_per),
                        self._div_yld, sale_px)
            div_flows = np.array([[(d[0]-self._trade_dt).days/365, d[1]] for d in div_flows])
        else:
            div_flows = divs
            div_flows.append([hold_per, sale_px])
        pv = 0
        for d in div_flows:
            pv += calcPV(d[1], r_req*self._div_freq, d[0]/self._div_freq)
        return pv 
    
    def calc2StageDDM(self, growth_s, years_gs, growth_l, r_req=None, divs=False):
        ''' Calculates the value of the stock based on the Dividend
        Discount Model
        
        Parameters
        ==========
        growth_s : float
            short term anbormally large growth rate
        growth_l : float
            long term sustainable growth rate
        years_gs : float
            years of short term growth rate
        r_req : float
            The required rate of return
            DEFAULT = Use the CAPM model and all its assumptions
        divs : list of lists of floats
            the dividend / date pairs if explicitly given
            
        Return
        ======
        pv : float
            The assumed present value based on DDM multistage model
        '''
        if not divs:
            # 0 sent in for par as no par value added to end, will add a zero value
            # to end of cash flow list
            div_flows = np.array(createCashFlows(self._trade_dt, self._div_freq,
                        self._trade_dt + datetime.timedelta(365*years_gs),
                        self._div_yld, 100, par_cf=False))
            div_flows = np.array([[(d[0]-self._trade_dt).days/365, d[1]] for d in div_flows])
        else:
            div_flows = divs
        
        # apply short term growth
        pdb.set_trace()
        div_flows_sum = 0
        for i in div_flows:
            div_flows_sum += (i[1] * (1 + growth_s)**i[0]) / (1+r_req)**i[0]
        Dn = (div_flows[0][1] * (1 + growth_s)**years_gs) * (1+growth_l)
        Dn = (Dn / (r_req - growth_l)) / (1+r_req)**years_gs
        return Dn + div_flows_sum
    
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
    
    def calcGordonGrowthModel(self, growth=None, r_req=None, D0=None):
        ''' Calculatesthe intrinsic value of the stock based on the GGM
        
        Parameters
        ==========
        growth : float
            estimate of growth of the dividends
            DEFAULT = (1 - dividend payout ratio) * Return on equity
        r_req : float
            The required rate of return
            DEFAULT = Use the CAPM model and all its assumptions
        D0 : float
            The most recent dividend

        Return
        ======
        float
            The calculated gordon growth value
        '''
        if not D0:
            D0 = self._cur_px * self._div_yld
        if not r_req:
            r_req = self.calcCAPM()
        if not growth:
            growth = calcGrowthEstimate()
        return (D0 * (1 + growth)) / (r_req - growth)
    
    def calcGrowthEstimate(self):
        b = (1 - self.calcDividendPayoutRatio())
        ROE = 1
        return (b * ROE)
    
    def retentionRate(self):
        # represented by "b" in a lot of equations
        return 1 - self.calcDividendPayoutRatio()
    
    def dividendPayoutRatio(self):
        return 0.45
        return (self._div_yld * self._cur_px) / self._EPS
    
    def calcJustifiedPE(self, growth=None, r_req=None, trailing=False):
        pdb.set_trace()
        if not r_req:
            r_req = self.calcCAPM()
        if not growth:
            growth = calcGrowthEstimate()

        if trailing:
            return self.dividendPayoutRatio() / (r_req - growth)
        else:
            return (self.dividendPayoutRatio() * (1 + growth)) / (r_req - growth)
    
    """ Load in P/S, P/E, P/B. P/CF """   
        

if __name__ == "__main__":
    e = CommonStock(div_yld=0.0108, cur_px=100, div_freq=1, trade_dt=datetime.date(2017,1,1))
    # divs = [[1,2], [2,2.1], [3,2.2]]
    # print(e.calcDividendDiscountModel(3, 20, 0.10, divs=divs))
    # print(e.calcCAPM())
    # print(e.calcGordonGrowthModel(growth=0.14, r_f=0.19, D0=2.28))
    # print(e.calc2StageDDM(0.065, 2, 0.04, r_req=0.066))
    print(e.calcJustifiedPE(growth=0.088, r_req=0.12, trailing=True))
    