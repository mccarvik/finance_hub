

class Curve():
    ''' Parent curve class representing any type of rate curve
        Types of curves supported:
        Zero Curve - aka spot curve or strip curve, sequence of ytm's on zero 
                    coupon bonds (or coupon bearing gov bonds)
        Par Curve - sequence of ytm's such that each bond is priced at par value.
    '''
    
    def __init__(self, dts, rates):
        ''' Constructor
        Parameters
        ==========
        dts : list of dates
            will be the day of each rate
        rates : list of rates
            will be the rate associated with each day
        
        Return
        ======
        NONE
        '''
        self._curve = list(zip(dts,rates))
        # https://www.treasury.gov/resource-center/data-chart-center/digitalstrategy/pages/developer.aspx
        # https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield