import sys
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import datetime, pdb
from app import app
from app.bond.bond import Bond
from app.utils.fi_funcs import *

class FRN(Bond):
    """This class will hold all the variables associated with a Floating Rate Note"""
    
    
    def __init__(self, cusip, issue_dt, mat_dt, sec_type, cpn, trade_dt=datetime.date.today(),
                dcc="ACT/ACT", par=100, price=None, ytm=None):
        ''' Constructor
        Parameters
        ==========
        cusip : str
            cusip of this bond
        issue_dt : str
            issue date of the bond
        mat_dt : str
            maturity date of the bond
        sec_type : str
            security type of the bond
        dcc : str
            day count convention, DEFAULT = "30/360"
        par : float
            par value of the bond, DEFAULT = 100
        price : float
            current price of the bond
        ytm : float
            yield to maturity of the bond
            NOTE - will come in as percent value and divided by 100, ex come in as 2(%) and become / 100 = 0.02
        trade_dt : date
            day the calculation is done from, DEFAULT = today
        
        Return
        ======
        NONE
        '''
        super().__init__(cusip, issue_dt, mat_dt, sec_type)
        self._dcc = dcc or "ACT/ACT"
        self._par = par
        self._trade_dt = trade_dt
        self._bm = self.findBenchmarkRate()
        self._pv = price
        if self._pv:
            self._disc_yld = self.calcDiscountYield()
        else:
            self._disc_yld = ytm / 100 if ytm else self._bm[1]
            self._pv = self.calcPresentValue()
        
        def calcPresentValue():
            # Not sure how correct this is
            return ((self._par * self._cpn) / (1 + self._disc_yld) + 
                    (self._par / (1 + self._disc_yld)))