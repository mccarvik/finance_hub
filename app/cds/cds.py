

class CDS:
    '''Will represent a single name credit default swap'''
    
    def __init__(mat, haz_rate=0.02, rec_rate):
        self._haz_rate = haz_rate
        self._rec_rate = rec_rate
        self._surv_rates = self.calcSurvRates()
        self._default_rates = self.calcDefaultRates()
        