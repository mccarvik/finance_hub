import sys
import numpy as np
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import datetime, pdb
from app.utils.fi_funcs import *


class Equity():
    '''This class will represent an individual stock'''
    
    def __init__(self, div_yld=0.0, div_freq=0.25, cur_px=100,
                trade_dt=datetime.date.today()):
        '''Constructor'''
        
        self._div_yld = div_yld
        self._div_freq = div_freq
        self._cur_px = cur_px
        self._trade_dt = trade_dt
        

    def calcDividendDiscountModel(self, r_req, hold_per, sale_px, divs=False):
        ''' Calculates the value of the stock based on the Dividend
        Discount Model
        
        Parameters
        ==========
        r_req : float
            The required rate of return
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
        if not divs and not self._divs:
            div_flows = np.array(createCashFlows(self._trade_dt, self._div_freq,
                        self._trade_dt + datetime.timedelta(365*hold_per),
                        self._div_yld, sale_px))
        elif divs:
            div_flows = divs
        
        pv = 0
        p = 1
        for d in div_flows:
            pv += calcPV(d, r_req*self._div_freq, p)
            p += 1
        pv += calcPV(sale_px, r_req*self._div_freq, hold_per/self._div_freq)
        return pv        
        
if __name__ == "__main__":
    e = Equity(div_yld=0.02, div_freq=1, trade_dt=datetime.date(2017,1,1))
    divs = [2, 2.1, 2.2]
    print(e.calcDividendDiscountModel(0.10, 3, 20, divs=divs))