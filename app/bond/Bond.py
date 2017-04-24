import datetime

class Bond():
    '''Parent class for Bonds, holds all the generic information'''
    
    def __init__(self, cusip, issueDate, matDate, secType):
        ''' Constructor
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
        self._issue_dt = datetime.date(int(issueDate[0:4]), int(issueDate[5:7]), int(issueDate[8:10]))
        self._mat_dt = datetime.date(int(matDate[0:4]), int(matDate[5:7]), int(matDate[8:10]))
        self._sec_type = secType