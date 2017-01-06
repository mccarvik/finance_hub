import sys
sys.path.append("/home/ubuntu/workspace/finance")
import datetime
from app import app
from app.utils.fi_funcs import *
from math import e

class CDS:
    '''Will represent a single name credit default swap'''
    
    def __init__(self, tenor, haz_rate=0.02, rec_rate=0.4):
        self._tenor = tenor
        self._haz_rate = haz_rate
        self._rec_rate = rec_rate
        self._surv_rates = self.calcSurvRates()
        self._def_rates = self.calcDefaultRates()
        print(self._def_rates)
        
        
    def calcSurvRates(self):
        return [calcSurvivalRate(t,self._haz_rate) for t in range(1,self._tenor+1)]
    
    def calcDefaultRates(self):
        rates = [1] + self._surv_rates
        def_rates = []
        for i in range(0,self._tenor):
            def_rates.append(rates[i] - rates[i+1])
        return def_rates

if __name__ == '__main__':
    cds = CDS(5, 0.02)