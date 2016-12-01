import datetime

class FixedRateBond():
    """This class will hold all the variables associated with a fixed rate bond"""
    
    def __init__(self, mat_dt, issue_dt, freq=None, cpn=None, dcc=None, par=None, price=None, ytm=None):
        self._mat_dt = mat_dt
        self._issue_dt = issue_dt
        self._dcc = dcc or "ACT/ACT"
        self._cpn = cpn or 0     # expressed in percent terms
        self._pay_freq = freq or "0.5"
        self._par = par or 100
        if price:
            self._price = price
            # self._ytm = self.calcYTMFromPrice()
        else:
            self._ytm = ytm
            # self._price = self.calcPriceFromYTM()
        
        self._cash_flows = self.createCashFlows()
    
    
    def createCashFlows(self):
        pass
    