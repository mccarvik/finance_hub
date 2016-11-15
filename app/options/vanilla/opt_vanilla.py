import numpy as np
import scipy.stats as ss
import time, sys
from app import app
from math import sqrt, pi, log, e

def post(request):
    import pdb; pdb.set_trace()
    try:
        vol_prem = request.form.get('calc_type', 'prem')
        otype = request.form.get('otype', 'C')
        und = request.form.get('underlying', 100)
        k = request.form.get('strike', 100)
        r = request.form.get('ir', 0.02)
        t = request.form.get('tenor', 1)
        v = request.form.get('vol', 0.3)
        p = request.form.get('prem', 12)
        d = request.form.get('div', 0)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        app.logger.info("Error in option vanilla vars {0}, {1}, {2}".format(exc_type, exc_tb.tb_lineno, exc_obj))
        return
    
    try:
        if request.form['action'] == 'calc':
            if request.form['calc_type'] == 'prem':
                p = None
                opt_van = OptionVanilla(otype, und, k, r, t, d, vol=v, prem=p)
                print(opt_van.premium)
                print("prem calc")
            elif request.form['calc_type'] == 'vol':
                v = None
                opt_van = OptionVanilla(otype, und, k, r, t, d, vol=v, prem=p)
                print(opt_van.premium)
                print("vol valc")
    except:
        print('here')

class OptionVanilla:
    
    def __init__(self, otype, underlying, strike, ir, tenor, div, vol=None, prem=None):
        self.otype = otype                          # type of option (C or P for call or put)
        self.underlying = float(underlying)         # Price of the underlying
        self.strike = float(strike)                 # strike price
        self.ir = float(ir)                         # interest rate (ex: 0.02 = 2%)
        self.tenor = float(tenor)                   # length of contract (ex 0.5 = 6 months)
        self.div = float(div)                       # continuous dividend rate
        if (vol):
            self.vol = float(vol)                   # volatility (ex: 0.3 = 30%)
            self.premium = self.priceFromVolBS()    # premium paid for the option
        elif (prem):
            self.prem = float(prem)
            #self.vol = volFromPriceBS()
        self.calcGreeks()
    
    def calcGreeks(self):
        self._delta = self.calcDelta()
    
    def calcDelta(self):
        # adjustment for if underlying pays a dividend
        dfq = e ** (-self.div * self.tenor)
        if self.otype == "C":
            return dfq * ss.norm.cdf(self.d1())
        else:
            return dfq * (ss.norm.cdf(self.d1()) - 1)
    
    def priceFromVolBS(self):
        if self.otype == "C":
            return self.underlying * ss.norm.cdf(self.d1()) - self.strike * np.exp(-self.ir * self.tenor) * ss.norm.cdf(self.d2())
        else:
            return self.strike * np.exp(-self.ir * self.tenor) * ss.norm.cdf(-self.d2()) - self.underlying * ss.norm.cdf(-self.d1())
        
    def d1(self):
        return ((np.log(self.underlying/self.strike) + (self.ir - self.div + 0.5 * self.vol**2)) * self.tenor) / (self.vol * np.sqrt(self.tenor))
 
    def d2(self):
        return self.d1() - (self.vol * np.sqrt(self.tenor))
 
    
if __name__ == "__main__":
    opt = OptionVanilla("C", 100, 130, 0.1, 1, 0, vol=0.3)
    print(opt.premium)