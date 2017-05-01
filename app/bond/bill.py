import sys
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import datetime, pdb
from app import app
from app.bond.bond import Bond
from app.utils.fi_funcs import *

class Bill(Bond):
    """This class will hold all the variables associated with a Bill
    Bills do not have coupons and are sold at a discount to par"""
    
    def __init__(self, cusip, issue_dt, mat_dt, sec_type, trade_dt=datetime.date.today(),
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
    
    def calcDiscountYield(self):
        pdb.set_trace()
        disc = (self._par - self._pv) / self._par
        days_to_mat = (self._mat_dt - self._trade_dt).days
        return ((360 / days_to_mat) * disc)
    
    def calcPresentValue(self):
        # http://www.investopedia.com/exam-guide/series-7/debt-securities/compute-treasury-discount-yield.asp
        days_to_mat = (self._mat_dt - self._trade_dt).days
        val = (self._disc_yld * days_to_mat) / 360
        val = (1 - val) * self._par
        return val

if __name__ == "__main__":
    # import pdb; pdb.set_trace()
    bond = Bill("TEST", "2017-01-01", "2017-01-29", "Bill", ytm=0.7971428571428265,
                trade_dt=datetime.date(2017,1,1))
    print(bond._pv)
    print(bond._disc_yld)
    
    