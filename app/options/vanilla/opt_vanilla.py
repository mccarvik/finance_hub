import sys
sys.path.append("/home/ubuntu/workspace/finance")
import numpy as np
import scipy.stats as ss
import time, sys, pdb
from app import app
from math import sqrt, pi, log, e

def post(request):
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
    
    def __init__(self, otype, underlying, strike, ir, tenor, div, vol=None, prem=None, greeks=False):
        self.otype = otype                          # type of option (C or P for call or put)
        self.underlying = float(underlying)         # Price of the underlying
        self.strike = float(strike)                 # strike price
        self.ir = float(ir)                         # interest rate (ex: 0.02 = 2%)
        self.tenor = float(tenor)                   # length of contract (ex 0.5 = 6 months)
        self.div = float(div)                       # continuous dividend rate
        if (vol):
            self.vol = float(vol)                   # volatility (ex: 0.3 = 30%)
            self.prem = self.priceFromVolBS()       # premium paid for the option
        elif (prem):
            self.prem = float(prem)
            self.vol = self.volFromPriceBS()
        if greeks:
            self.calcGreeks()
    
    def calcGreeks(self):
        self._delta = self.calcDelta()
        self._gamma = self.calcGamma()
        self._theta = self.calcTheta()
        self._vega = self.calcVega()
        self._rho = self.calcRho()
        print("Done Calcing Greeks")
    
    def calcDelta(self):
        # adjustment for if underlying pays a dividend
        dfq = e ** (-self.div * self.tenor)
        if self.otype == "C":
            return dfq * ss.norm.cdf(self.d1())
        else:
            return dfq * (ss.norm.cdf(self.d1()) - 1)
    
    def calcTheta(self):
        dfq = e ** (-self.div * self.tenor)
        dfr = e ** (-self.ir * self.tenor)
        if self.otype == "C":
            front = (-1) * ((self.underlying * self.prob_dens_func(self.d1()) * self.vol * dfq) / (2 * np.sqrt(self.tenor)))
            back = self.div * self.underlying * ss.norm.cdf(self.d1()) * dfq - self.ir * self.strike * dfr * ss.norm.cdf(self.d2())
            return front + back
        else:
            front = (-1) * ((self.underlying * self.prob_dens_func(self.d1()) * self.vol * dfq) / (2 * np.sqrt(self.tenor)))
            back = self.div * self.underlying * ss.norm.cdf((-1)*self.d1()) * dfq - self.ir * self.strike * dfr * ss.norm.cdf((-1)*self.d2())
            return front - back
    
    def calcGamma(self):
        dfq = e ** (-self.div * self.tenor)
        num = self.prob_dens_func(self.d1()) * dfq
        return num /  (self.underlying * self.vol * np.sqrt(self.tenor))
    
    def calcVega(self, vol_guess=None):
        ''' Calculates the change in premium for the option per change in volatility (partial derivative)
        
        Parameters
        =========
        vol_guess : float
            guess at the implied vol needed when calcing the vol from price
        
        Return
        ======
        float
            change in premium per change in volatility
        '''
        
        if vol_guess:
            self.vol = vol_guess 
        dfq = e ** (-self.div * self.tenor)
        return self.underlying * np.sqrt(self.tenor) * dfq * self.prob_dens_func(self.d2())
    
    def calcRho(self):
        dfr = e ** (-self.ir * self.tenor)
        if self.otype == "C":
            return self.strike * self.tenor * dfr * ss.norm.cdf(self.d2())
        else:
            return (-1) * self.strike * self.tenor * dfr * ss.norm.cdf((-1) * self.d2())
        
    def d1(self):
        return (np.log(self.underlying/self.strike) + ((self.ir - self.div + 0.5 * self.vol**2) * self.tenor)) / (self.vol * np.sqrt(self.tenor))
 
    def d2(self):
        return self.d1() - (self.vol * np.sqrt(self.tenor))
    
    def prob_dens_func(self, x):
        return (1 / np.sqrt(pi*2)) * e ** (((-1) * x**2)/2)
        
    def priceFromVolBS(self, vol_guess=None):
        ''' Calculates the price of an option given the implied volatility in BS
        
        Paramters
        =========
        vol_guess : float
            guess at the implied vol needed when calcing the vol from price
        
        Return
        ======
        float
            price of the option
        '''
                
        if vol_guess:
            self.vol = vol_guess  
        if self.otype == "C":
            return self.underlying * ss.norm.cdf(self.d1()) - self.strike * np.exp(-self.ir * self.tenor) * ss.norm.cdf(self.d2())
        else:
            return self.strike * np.exp(-self.ir * self.tenor) * ss.norm.cdf(-self.d2()) - self.underlying * ss.norm.cdf(-self.d1())
    
    def volFromPriceBS(self, imp_vol_guess=0.2, it=100):
        ''' Calculates implied volatility when given the price of a European call option in BS
        
        Parameters
        ==========
        imp_vol_guess : float
            estimate of implied volatility
        it : int 
            number of iterations of process
            
        Returns
        =======
        imp_vol_guess : float
            estimated value for implied vol
        '''
        for i in range(it):
            # reusing code from the price calc to use our vol guess
            imp_vol_guess -= ((self.priceFromVolBS(vol_guess=imp_vol_guess) - self.prem) / 
                            self.calcVega(vol_guess=imp_vol_guess))
        return imp_vol_guess
        
    def priceFromVolBinTree(self, N=2000):
        # N = number of steps of tree
        sigma = self.vol
        K = self.strike
        r = self.ir
        S0 = self.underlying
        T = self.tenor
        otype = self.otype
        
        #calculate delta T    
        deltaT = float(T) / N
     
        # up and down factor will be constant for the tree so we calculate outside the loop
        u = np.exp(sigma * np.sqrt(deltaT))
        d = 1.0 / u
     
       
        # Initialise our f_{i,j} tree with zeros
        fs = [[0.0 for j in range(i + 1)] for i in range(N + 1)]
        
        #store the tree in a triangular matrix
        #this is the closest to theory
        
        #no need for the stock tree
     
        #rates are fixed so the probability of up and down are fixed.
        #this is used to make sure the drift is the risk free rate
        a = np.exp(r * deltaT)
        p = (a - d) / (u - d)
        oneMinusP = 1.0 - p
        
        # Compute the leaves, f_{N, j}
        for j in range(len(fs)):
            if otype =="C":
                fs[N][j] = max(S0 * u**j * d**(N - j) - K, 0.0)
            else:
                fs[N][j] = max(-S0 * u**j * d**(N - j) + K, 0.0)
                
        #calculate backward the option prices
        for i in range(N-1, -1, -1):
            for j in range(i + 1):
                fs[i][j] = np.exp(-r * deltaT) * (p * fs[i + 1][j + 1] + oneMinusP * fs[i + 1][j])
        return fs[0][0]
 
    
if __name__ == "__main__":
    # import pdb; pdb.set_trace()
    # opt = OptionVanilla("C", 49, 50, 0.05, 0.3846, 0, vol=0.2)
    # opt = OptionVanilla("C", 11.49, 11.50, 0.00, (18/250), 0, vol=0.05)
    opt = OptionVanilla("C", 11.49, 11.50, 0.00, (18/250), 0, prem=0.0566)
    # print(opt.priceFromVolBinTree())
    print(opt.priceFromVolBS())
    # print(opt.volFromPriceBS())