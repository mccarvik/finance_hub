import sys
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import datetime
from app import app
from app.bond.bond import Bond
from app.utils.fi_funcs import *
from dateutil.relativedelta import relativedelta

class FixedRateBond(Bond):
    """This class will hold all the variables associated with a fixed rate bond"""
    
    def __init__(self, cusip, issue_dt, mat_dt, sec_type, first_pay_dt=None, freq=0.5, 
                cpn=0, dcc="ACT/ACT", par=100, price=None, ytm=None, trade_dt=datetime.date.today()):
        ''' Constructor
        Parameters
        ==========
        cusip : str
            cusip of this bond
        issue_dt : str
            issue date of the bond
        mat_dt : str
            maturity date of the bond
        sec_type : str
            security type of the bond
        first_pay_dt : str
            first payment date, need this as some bonds have a short stub period before first payment
            instead of a full accrual period, DEFAULT = None
        freq : float
            payment frequency of the bond, expressed in fractional terms of 1 year, ex: 0.5 = 6 months
            DEFAULT = 0.5
        cpn : float
            coupon rate of the bond, expressed in percent terms not dollar amount, DEFAULT = 0
            NOTE - will come in as percent value and divided by 100, ex 2% / 100 = 0.02
        dcc : str
            day count convention, DEFAULT = "ACT/ACT"
        par : float
            par value of the bond, DEFAULT = 100
        price : float
            current price of the bond
        ytm : float
            yield to maturity of the bond
            NOTE - will come in as percent value and divided by 100, ex come in as 2(%) and become / 100 = 0.02
        trade_dt : date
            day the calculation is done from, DEFAULT = today
        
        Return
        ======
        NONE
        '''
        super().__init__(cusip, issue_dt, mat_dt, sec_type)
        ytm = ytm / 100 if ytm else None
        self._dcc = dcc or "ACT/ACT"
        self._cpn = cpn / 100 if cpn else 0
        self._pay_freq = freq  
        self._par = par
        self._trade_dt = trade_dt
        
        if self._cpn==0:
            import pdb; pdb.set_trace()
            print()
        
        if first_pay_dt:
            self._first_pay_dt = datetime.date(int(first_pay_dt[0:4]), int(first_pay_dt[5:7]), int(first_pay_dt[8:10]))
            self._cash_flows = createCashFlows(self._first_pay_dt, self._pay_freq, self._mat_dt, self._cpn, self._par)
            self._cash_flows.insert(0, (self._first_pay_dt, self._cpn*freq))
        else:
            self._cash_flows = createCashFlows(self._issue_dt, self._pay_freq, self._mat_dt, self._cpn, self._par)

        try:
            self._pv, self._ytm = self.calcPVandYTM(price, ytm)
            self._conv_factor = self.calcConversionFactor()
            self._dur_mod = self.calcDurationModified()
            self._dur_mac = self.calcDurationMacauley()
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            app.logger.info("ISSUE Calculating bond for cusip: {3}: {0}, {1}, {2}".format(exc_type, exc_tb.tb_lineno, exc_obj, self._cusip))
    
    def calcPVandYTM(self, pv, ytm):
        ''' Will calculate PV from YTM or YTM from pv depending on what is provided
        Parameters
        ==========
        pv : float
            present value of the bond
        ytm : float
            yield to maturity of the bond
        
        Return
        ======
        tuple
            pair of pv and ytm
        '''
        if pv:
            ytm = calcYieldToDate(pv, self._par, self._mat_dt, self._cpn, freq=self._pay_freq, start_date=self._trade_dt)
        else:
            pv = cumPresentValue(self._trade_dt, ytm, self._cash_flows, self._pay_freq, cont=False)
        return (pv, ytm)
    
    def calcConversionFactor(self):
        ''' Calculates the conversion factor for his bond in relation to bond futures baskets
            Assumptions: 20 yrs to maturity, 6% annual disc rate, semi-annual compounding, first cpn payment in 6 months
        Parameters
        ==========
        self : Object
            self instance that has all the variables needed
        
        Return
        ======
        convFactor : float
            uses the cumulative present value function to calculate the bond conversion factor with the above assumptions
        '''
        assumed_mat_date = self._issue_dt + relativedelta(years=20)
        cfs = createCashFlows(self._issue_dt, 0.5, assumed_mat_date, self._cpn, 100)
        return cumPresentValue(self._trade_dt, 0.06, cfs, 0.5) / self._par
    
    def calcDurationModified(self):
        dur = 0
        for cf in self._cash_flows:
            # assuming trade_dt = today, might wanna modify this later
            t = (cf[0] - self._trade_dt).days / 365
            # get present valye of cash flow * how many years away it is
            d_temp =  t * (calcPV(cf[1], (self._ytm * self._pay_freq), (t / self._pay_freq)))
            # divide by Bond price
            dur += (d_temp / self._pv)
        return dur
    
    def calcDurationMacauley(self):
        dur = 0
        cum_pv = 0
        for cf in self._cash_flows:
            # assuming trade_dt = today, might wanna modify this later
            t = (cf[0] - self._trade_dt).days / 365
            # get present valye of cash flow * how many years away it is
            d_temp = t * (calcPVContinuous(cf[1], (self._ytm * self._pay_freq), (t / self._pay_freq)))
            # divide by Bond price
            dur += (d_temp / self._pv)
        return dur
        
    def calcParYield(self, fwd_rates, guess=None, start_date=datetime.datetime.today().date(), cont_comp=False):
        """
        This means that given a list of forward rates, we can calculate what the coupon rate 
        needs to be to have the bond equal par
        similar to yield to maturity calc, needs a newton Raphson approximation
        
        assume rates are forward rates and they line up with coupon dates
        
        Need the "- self._par" at the end to optimize for = 100 not 0
        """
        freq = self._pay_freq
        # guess cpn = last fwd rate * 100 as a coupon, will get us in the ball park
        guess = fwd_rates[-1][1] * 100
        
        fwd_rates = [((f[0] - start_date).days / 365, f[1]) for f in fwd_rates]
        
        if cont_comp:
            py_func = lambda y: \
                sum([(y*freq)*e**(-1*f[1]) for f in fwd_rates]) + \
                (self._par) * e**(-1*fwd_rates[-1][1]) - self._par
        else:
            import pdb; pdb.set_trace()
            py_func = lambda y: \
                sum([(y*freq) / (1+f[1]) for f in fwd_rates]) + \
                (self._par) / (1+fwd_rates[-1][1]) - self._par
        
        # need to divide by freq to get the annual coupon rate
        return newton_raphson(py_func, guess) / freq
        

if __name__ == "__main__":
    # import pdb; pdb.set_trace()
    # bond = FixedRateBond("TEST", "2017-01-01", "2020-01-01", "Bond", freq=1, cpn=10, dcc="ACT/ACT", 
    #                     par=100, ytm=10.405, trade_dt=datetime.date(2017,1,1))
    bond = FixedRateBond("TEST", "2017-01-01", "2020-01-01", "Bond", freq=1, cpn=10, dcc="ACT/ACT", 
                        par=100, price=99, trade_dt=datetime.date(2017,1,1))
    # fwd_rates = [.05, .058, .064, .068]
    # cf = [cf[0] for cf in bond._cash_flows]
    # fwd_rates = list(zip(cf,fwd_rates))
    # print(bond.calcParYield(fwd_rates,cont_comp=True))
    # print(bond._conv_factor)
    print(bond._pv)
    print(bond._ytm)
    # print(bond._dur_mod)
    # print(bond._dur_mac)
    
    
    