import datetime

class Bond():
    '''Parent class for Bonds, holds all the generic information'''
    
    def __init__(self, cusip, issueDate, matDate, secType):
        '''
        Parameters
        ==========
        cusip : str
            cusip of this bond
        issueDate : str
            when bond was issued
        matDate : str
            maturity date of bond
        secType : str
            type of security
        
        Return
        ======
        NONE
        '''
        
        self._cusip = cusip
        self._iss_date = datetime.date(issueDate)
        self._mat_date = datetime.date(matDate)
        self._sec_type = secType