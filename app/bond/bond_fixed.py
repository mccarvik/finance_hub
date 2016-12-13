import sys
sys.path.append("/home/ubuntu/workspace/finance")
import datetime
from app import app
from app.utils.fi_funcs import *

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
        self._cash_flows = createCashFlows(self._issue_dt, self._pay_freq, self._tenor, self._cpn, self._par)
        self._pv, self._ytm = self.calcPVandYTM(price, ytm)
        
        self._conv_factor = self.calcConversionFactor()
        self._dur_mod = self.calcDurationModified()
        self._dur_mac = self.calcDurationMacauley()
    
    def calcPVandYTM(self, price, ytm):
        if price:
            return (price, calcYieldToDate(price, self._par, self._tenor, self._cpn, self._pay_freq))
        else:
            pv = cumPresentValue(self._trade_dt, ytm, self._cash_flows, self._pay_freq, cont=False)
            return (pv, ytm)
    
    def calcConversionFactor(self):
        # Assumptions: 20 yrs to maturity, 6% annual disc rate, semi-annual compounding, first cpn payment in 6 months
        cfs = createCashFlows(self._issue_dt, 0.5, 20, self._cpn, 100)
        return cumPresentValue(self._trade_dt, 0.06, cfs, 0.5) / self._par
    
    def calcDurationModified(self):
        dur = 0
        for cf in self._cash_flows:
            # assuming trade_dt = today, might wanna modify this later
            t = (cf[0] - self._trade_dt).days / 365
            # get present valye of cash flow * how many years away it is
            d_temp =  t * (calcPV(cf[1], (self._ytm * self._pay_freq), (t / self._pay_freq)))
            # divide by Bond price
            dur += (d_temp / self._pv)
        return dur
    
    def calcDurationMacauley(self):
        dur = 0
        cum_pv = 0
        for cf in self._cash_flows:
            # assuming trade_dt = today, might wanna modify this later
            t = (cf[0] - self._trade_dt).days / 365
            # get present valye of cash flow * how many years away it is
            d_temp = t * (calcPVContinuous(cf[1], (self._ytm * self._pay_freq), (t / self._pay_freq)))
            # divide by Bond price
            dur += (d_temp / self._pv)
        return dur
        
    def calcParYield(self, price, par, tenor, fwd_rates, freq=0.5, guess=None, start_date=datetime.datetime.today()):
        """
        This means that given a list of forward rates, we can calculate what the coupon rate 
        needs to be to have the bond equal par
        similar to yield to maturity calc, needs a newton Raphson approximation
        """
        
        freq = float(freq)
        # guess ytm = last fwd rate, will get us in the ball park
        guess = fwd_rates[-1][1]
        py_func = lambda y: \
            sum([y/(1+y*freq)**(t/freq) for f in fwd_rates]) + \
            par/(1+y*freq)**(tenor/freq) - par
        
        return optimize.newton(py, guess)
        
        

if __name__ == "__main__":
    # import pdb; pdb.set_trace()
    bond = FixedRateBond(3, datetime.date(2016,3,1), 0.5, 0.10, "ACT/ACT", 100, ytm=0.123673)
    print(bond._conv_factor)
    print(bond._pv)
    print(bond._dur_mod)
    # print(bond._dur_mac)
    