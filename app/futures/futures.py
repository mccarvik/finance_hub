import numpy as np
import scipy.stats as ss
import time, sys
from app import app
from math import sqrt, pi, log, e

def post(request):
    # import pdb; pdb.set_trace()
    if request.form['action'] == 'fut_calc':
        fut_calc(request)

def fut_calc(request):
    print("Futures CALCULATOR")

    try:
        fut_for = request.form.get('fut_for', 'for')
        und = request.form.get('underlying', None)
        r = request.form.get('ir', None)
        t = request.form.get('tenor', 1)
        d = request.form.get('div', 0)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        app.logger.info("Error in option vanilla vars {0}, {1}, {2}".format(exc_type, exc_tb.tb_lineno, exc_obj))
        return
    
    forward = Futures(fut_for, und, r, t, d, p=None)

class Futures:
    """class to define the attributes and calcs of a 
    forward or futures object"""
    
    def __init__(self, fut_for='for', und=None, r=None, t=1, d=None, p=None):
        self._type = fut_for
        self._und = und
        self._rate = r
        self._tenor = t
        self._div = d
        self._price = p
        
        self.calcMissing()
    
    def calcMissing(self):
        if not self._price:
            self._price = self.calcPrice()
    
    def calcPrice(self):
        if self._type == 'for':
            self._price = (self._und) * (e**(self._rate*self._tenor))