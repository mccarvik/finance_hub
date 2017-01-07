import sys
sys.path.append("/home/ubuntu/workspace/finance")
import datetime
from app import app
from app.utils.fi_funcs import *
from math import e

class CDS:
    '''Will represent a single name credit default swap'''
    
    def __init__(self, tenor, notl=100, cpn=1, pay_freq=1, haz_rate=0.02, rec_rate=0.4):
        self._tenor = tenor
        self._cpn = cpn
        self._pay_freq = pay_freq
        self._haz_rate = haz_rate
        self._rec_rate = rec_rate
        self._disc_factors = [0.9512, 0.9048, 0.8607, 0.8187, 0.7788]
        self._surv_rates = self.calcSurvRates()
        self._def_rates = self.calcDefaultRates()
        print(self._def_rates)
        self._price = self.calcPrice()
    
    def calcPrice(self):
        pvs = self.calcPVofPayments()
        print(pvs)
    
    def calcPVofPayments(self):
        tot = 0
        for d, s in zip(self._disc_factors, self._surv_rates):
            tot += d * s * self._cpn
        return tot
        
    def calcSurvRates(self):
        return [calcSurvivalRate(t,self._haz_rate) for t in range(1,self._tenor+1)]
    
    def calcDefaultRates(self):
        rates = [1] + self._surv_rates
        def_rates = []
        for i in range(0,self._tenor):
            def_rates.append(rates[i] - rates[i+1])
        return def_rates

if __name__ == '__main__':
    # import pdb; pdb.set_trace()
    cds = CDS(5)