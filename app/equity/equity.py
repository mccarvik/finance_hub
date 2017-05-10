

class Equity():
    '''This class will represent an individual stock'''
    
    def __init__(self, div_yld=0.0):
        '''Constructor'''
        
        self._div_yld = div_yld

    
    def calcDividendDiscountModel(self, r_req):
        return 0