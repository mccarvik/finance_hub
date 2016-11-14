import numpy as np
import scipy.stats as ss
import time, sys
from app import app

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
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        app.logger.info("Error in option vanilla vars {0}, {1}, {2}".format(exc_type, exc_tb.tb_lineno, exc_obj))
        return
    
    try:
        if request.form['action'] == 'calc':
            if request.form['calc_type'] == 'prem':
                p = None
                opt_van = OptionVanilla(otype, und, k, r, t, vol=v, prem=p)
                print(opt_van.premium)
                print("prem calc")
            elif request.form['calc_type'] == 'vol':
                v = None
                opt_van = OptionVanilla(otype, und, k, r, t, vol=v, prem=p)
                print(opt_van.premium)
                print("vol valc")
    except:
        print('here')

class OptionVanilla:
    
    def __init__(self, otype, underlying, strike, ir, tenor, vol=None, prem=None):
        self.otype = otype
        self.underlying = float(underlying)
        self.strike = float(strike)
        self.ir = float(ir)
        self.tenor = float(tenor)
        if (vol):
            self.vol = float(vol)
            self.premium = self.priceFromVolBS()
        elif (premium):
            self.premium = float(premium)
            #self.vol = volFromPriceBS()
    
    def priceFromVolBS(self):
        if self.otype=="C":
            return self.underlying * ss.norm.cdf(self.d1()) - self.strike * np.exp(-self.ir * self.tenor) * ss.norm.cdf(self.d2())
        else:
            return self.strike * np.exp(-self.ir * self.tenor) * ss.norm.cdf(-self.d2()) - self.underlying * ss.norm.cdf(-self.d1())
        
    def d1(self):
        return (np.log(self.underlying/self.strike) + (self.ir + self.vol**2 / 2) * self.tenor) / (self.vol * np.sqrt(self.tenor))
 
    def d2(self):
        return (np.log(self.underlying / self.strike) + (self.ir - self.vol**2 / 2) * self.tenor) / (self.vol * np.sqrt(self.tenor))
 


    
if __name__ == "__main__":
    opt = OptionVanilla("C", 100, 130, 0.1, 1, vol=0.3)
    print(opt.premium)