import sys
import numpy as np
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import datetime, pdb
from app.equity.equity import Equity
from app.utils.fi_funcs import *
from app.curves.curve_funcs import *


class PreferredStock(Equity):
    '''This class will represent an individual stock'''
    
    def __init__(self, div_yld, div_freq=0.25, cur_px=100, par=100,
                trade_dt=datetime.date.today()):
        '''Constructor'''
        
        self._div_yld = div_yld
        self._div_freq = div_freq
        self._cur_px = cur_px
        self._par = par
        self._trade_dt = trade_dt
    
    def calcPresentValue(self, r_req=0.04):
        return (self._div_yld*self._par) / r_req

if __name__ == "__main__":
    p = PreferredStock(0.05, div_freq=0.25, par=25, trade_dt=datetime.date(2017,1,1))
    print(p.calcPresentValue(r_req=0.075))
    print(p.calcDividendDiscountModel(8.5, 25, 0.155))