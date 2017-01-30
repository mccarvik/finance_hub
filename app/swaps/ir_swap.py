import sys
sys.path.append("/home/ubuntu/workspace/finance")
import datetime
from dateutil.relativedelta import relativedelta
from app import app
from app.bond import bond_fixed

class IR_Swap():
    """ Class to represent a fixed for floating swap """
    
    def __init__(self, tenor=1.25, issue_dt=datetime.date(2015,10,30), notl=100, fixed_rate=0.03, 
                fixed_pay_freq=0.5, float_pay_freq=0.5, float_pay_reset=0.5, float_ref='6M libor',
                dcc_fixed='ACT/ACT'):
        self._tenor = tenor
        self._mat_dt = issue_dt + datetime.timedelta(tenor)
        self._trade_dt = issue_dt       # for now
        self._settle_dt = issue_dt      # for convenience
        self._notional = notl
        self._fixed_rate = fixed_rate
        self._fixed_pay_freq = fixed_pay_freq
        self._float_pay_freq = float_pay_freq
        self._float_pay_reset = float_pay_reset
        self._float_ref = float_ref
        self._dcc_fixed = dcc_fixed
        self._val = self.calcSwapValue()
    
    
    def calcSwapValue(self):
        val_fixed = self.calcFixedVal()
        val_float = self.calcFloatVal()
    
    def calcFixedVal(self):
        fixed = bond_fixed.FixedRateBond(5, datetime.date(2015,10,30), self._fixed_pay_freq, 
                    self._fixed_rate, self._dcc_fixed, 100, price=100)
        print(fixed)
        # fixed = bond_fixed(5, )
        
    def calcFloatVal(self):
        pass