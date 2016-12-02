import sys
sys.path.append("/home/ubuntu/workspace/finance")
import datetime
from app import app
from app.utils.helper_funcs import cumPresentValue, createCashFlows

class FixedRateBond():
    """This class will hold all the variables associated with a fixed rate bond"""
    
    def __init__(self, tenor, issue_dt, freq=None, cpn=None, dcc=None, par=None, price=None, ytm=None):
        self._issue_dt = issue_dt
        self._tenor = tenor
        self._mat_dt = issue_dt + datetime.timedelta(tenor)
        self._trade_dt = issue_dt       # for now
        self._settle_dt = issue_dt      # for convenience
        self._dcc = dcc or "ACT/ACT"
        self._cpn = cpn or 0            # expressed in percent terms, ex: 0.02 = 2%
        self._pay_freq = freq or "0.5"  # expressed in fractional terms of 1 year
        self._par = par or 100
        if price:
            self._price = price
            # self._ytm = self.calcYTMFromPrice()
        else:
            self._ytm = ytm
            # self._price = self.calcPriceFromYTM()
        
        self._cash_flows = createCashFlows(self._issue_dt, self._pay_freq, self._tenor, self._cpn, self._par)
        self._conv_factor = self.calcConversionFactor()
    
    def calcConversionFactor(self):
        # Assumptions: 20 yrs to maturity, 6% annual disc rate, semi-annual compounding, first cpn payment in 6 months
        cfs = createCashFlows(self._issue_dt, 0.5, 20, self._cpn, 100)
        return cumPresentValue(self._trade_dt, 0.06, cfs, 0.5) / self._par
        
        
        

if __name__ == "__main__":
    # import pdb; pdb.set_trace()
    bond = FixedRateBond(2, datetime.date(2016,3,1), 0.5, 0.10, "ACT/ACT", 100, 98)
    print(bond._conv_factor)
    