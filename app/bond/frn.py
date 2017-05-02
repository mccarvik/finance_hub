import sys
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import datetime, pdb
from app import app
from app.bond.bond import Bond
from app.utils.fi_funcs import *

class FRN(Bond):
    """This class will hold all the variables associated with a Floating Rate Note"""
    
    
    def __init__(self, cusip, issue_dt, mat_dt, sec_type, cpn=0, trade_dt=datetime.date.today(),
                dcc="ACT/ACT", par=100, price=None, ytm=None, pay_freq=0.5, reset_freq=None,
                reset='arrears', first_pay_dt=None):
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
        cpn : float
            coupon rate of the bond, expressed in percent terms not dollar amount, DEFAULT = 0
            NOTE - will come in as percent value and divided by 100, ex 2% / 100 = 0.02
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
        pay_freq : float
            payment frequency of the bond, expressed in fractional terms of 1 year, ex: 0.5 = 6 months
            DEFAULT = 0.5
        reset_freq : float
            reset frequency of the bond, expressed in fractional terms of 1 year, ex: 0.5 = 6 months
            how often the coupon of the floating rate bond will be reset
            DEFAULT = NONE, but set equal to pay_freq
        reset : str
            when the reset will take place: "now" or "arrears", arrears meaning the coupon was set at the end
            of the previous period, now meaning the coupon is set on the coupon date
            DEFAULT = "arrears"
        first_pay_dt : str
            first payment date, need this as some bonds have a short stub period before first payment
            instead of a full accrual period, DEFAULT = None
        
        Return
        ======
        NONE
        '''
        super().__init__(cusip, issue_dt, mat_dt, sec_type)
        reset_freq = pay_freq if not reset_freq else reset_freq
        self._dcc = dcc or "ACT/ACT"
        self._cpn = cpn / 100 if cpn else 0
        self._par = par
        self._trade_dt = trade_dt
        self._reset = reset
        self._pay_freq = pay_freq
        self._reset_freq = reset_freq
        self._bm = self.findBenchmarkRate()
        self._pv = price
        
        if first_pay_dt:
            self._first_pay_dt = datetime.date(int(first_pay_dt[0:4]), int(first_pay_dt[5:7]), int(first_pay_dt[8:10]))
            self._cash_flows = createCashFlows(self._first_pay_dt, self._pay_freq, self._mat_dt, self._cpn, self._par)
            self._cash_flows.insert(0, (self._first_pay_dt, self._cpn * self._par * self._pay_freq))
        else:
            self._cash_flows = createCashFlows(self._issue_dt, self._pay_freq, self._mat_dt, self._cpn, self._par)
        
        if self._pv:
            self._disc_yld = self.calcDiscountYield()
        else:
            pdb.set_trace()
            self._disc_yld = ytm / 100 if ytm else self._bm[1]
            self._pv = self.calcPresentValue()
        
    def calcPresentValue(self):
        # Not sure how correct this is
        pdb.set_trace()
        r_adj = self._disc_yld * self._pay_freq
        # http://finance.zacks.com/price-bonds-floating-rates-11553.html
        # used to figure out how far into the pay period we are
        days_to_payment_ratio = (((self._cash_flows[0][0] - self._trade_dt).days)/365) / self._pay_freq
        return ((self._par * self._cpn * self._pay_freq) / (1 + r_adj)**(days_to_payment_ratio) + 
                (self._par / (1 + r_adj)**(days_to_payment_ratio)))
    
    def calcDiscountMargin(self):
        pass

if __name__ == "__main__":
    # import pdb; pdb.set_trace()
    bond = FRN("TEST", "2017-01-01", "2020-01-29", "FRN", cpn=3.5, trade_dt=datetime.date(2017,6,1),
                pay_freq=0.5)
    print(bond._pv)
    print(bond._disc_yld)