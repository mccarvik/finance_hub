import datetime
from app.curves import curve_funcs

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
    
    def findBenchmarkRate(self, crv_type='tsy', interp='linear', ref_dt=None):
        ''' method to find the benchmark bond for a given curve
        Parameters
        ==========
        crv : string
            type of curve to load
        interp : string
            the interpolation method to find the benchmark rate
            flat = finds the closest point and takes that value
            linear = linear interpolate between nearest two points
        
        Return
        ======
        rate : float
            the benchmark rate for this bond
        '''
        ref_dt = self._mat_dt if not ref_dt else ref_dt
        if crv_type == 'tsy':
            crv = curve_funcs.loadTreasuryCurve(dflt=True)
        
        if interp == 'flat':
            return curve_funcs.flatInterp(ref_dt, crv)
        elif interp == 'linear':
            return curve_funcs.linearInterp(ref_dt, crv)
            
    