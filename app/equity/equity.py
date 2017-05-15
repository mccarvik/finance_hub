import sys
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import datetime, pdb
from app.utils.fi_funcs import *
from app.equity.screener_eqs import *

class Equity():
    '''Parent class of all stock and other equity products'''
    
    def __init__(self, ticker, div_yld=0, div_freq=1, cur_px=100, load_data=False):
        '''Constructor'''
        self._ticker = ticker
        self._div_yld = div_yld
        self._div_freq = div_freq
        self._cur_px = cur_px
        if load_data:
            self.load_data_to_db()
    
    def calcDividendDiscountModel(self, hold_per, sale_px, r_req=0.04, divs=False):
        ''' Calculates the value of the stock based on the Dividend
        Discount Model
        
        Parameters
        ==========
        r_req : float
            The required rate of return
            DEFAULT = 0.04, historical value
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
        

    def load_data_to_db(self):
        screener_eqs.get_data()