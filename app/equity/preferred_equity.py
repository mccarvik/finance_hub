import sys
import numpy as np
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import datetime, pdb
from app.utils.fi_funcs import *
from app.curves.curve_funcs import *


class Equity():
    '''This class will represent an individual stock'''
    
    def __init__(self, div_yld=0.0, div_freq=0.25, cur_px=100, beta=1,
                trade_dt=datetime.date.today()):
        '''Constructor'''
        
        self._div_yld = div_yld
        self._div_freq = div_freq
        self._cur_px = cur_px
        self._trade_dt = trade_dt