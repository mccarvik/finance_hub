

class Equity():
    '''This class will represent an individual stock'''
    
    def __init__(self, div_yld=0.0, div_freq=0.25):
        '''Constructor'''
        
        self._div_yld = div_yld
        self._div_freq = div_freq

    
    def calcDividendDiscountModel(self, r_req, hold_per=1.0):
        return 0