import numpy as np
import scipy.stats as ss
import time

class OptionVanilla:
    
    def __init__(self, otype, underlying, strike, ir, tenor, vol=None, premium=None):
        self.otype = otype
        self.underlying = underlying
        self.strike = strike
        self.ir = ir
        self.tenor  = tenor
        if (vol):
            self.vol = vol
            self.premium = self.priceFromVolBS()
        elif (premium):
            self.premium = premium
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
 

def main():
    opt = Option("C", 100, 130, 0.1, 1, vol=0.3)
    print(opt.premium)
    
if __name__ == "__main__":
    main()