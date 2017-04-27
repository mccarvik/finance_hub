from app.curves.curve import Curve

class TreasuryCurve(Curve):
    ''' Creates a treasury curve by scraping treasury.gov website'''
    
    def __init__(self):
        ''' Constrcutor
        Parameters
        =========
        NONE
        
        Return
        ======
        NONE
        '''
        rates = scrapeTsyCurve()
        super().__init__(rates)