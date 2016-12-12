import datetime
from scipy import optimize
from math import sqrt, pi, log, e


def bootstrap(first_zero_rate, first_mat, bs_rate_mats):
    """
    bs_rate_mats = list of tuples in the format (fwd_rate, maturity)
    """
    new_bs_rate_mats = []
    next_bs_zero_rate = ((bs_rate_mats[0][0] * bs_rate_mats[0][1]) + (first_zero_rate * first_mat)) / (bs_rate_mats[0][1] + first_mat)
    new_bs_rate_mats.append(tuple([bs_rate_mats[0][1] + first_mat, next_bs_zero_rate]))
    for i in range(len(bs_rate_mats)):
        if i == 0:
            continue
        
        next_bs_zero_rate = ((bs_rate_mats[i][0] * bs_rate_mats[i][1]) + \
            (new_bs_rate_mats[-1][1] * new_bs_rate_mats[-1][0])) / \
            (bs_rate_mats[i][1] + new_bs_rate_mats[-1][0])
        new_bs_rate_mats.append(tuple([bs_rate_mats[i][1] + new_bs_rate_mats[-1][0], next_bs_zero_rate]))
    return new_bs_rate_mats


def cumPresentValue(today, annual_disc_rate, cfs, freq=1, cont=True):
    cum_pv = 0
    # freq if rate passed in is not annual, ex: 0.5 = semiannual
    ir = annual_disc_rate * freq
    for i in cfs:
        period = ((i[0] - today).days / 365) / freq
        if cont:
            cum_pv += calcPVContinuous(i[1], ir, period)
        else:
            cum_pv += calcPV(i[1], ir, period)
    return cum_pv

def calcPV(cf, ir, period):
    return (cf / (1+ir)**period)

def calcPVContinuous(cf, ir, period):
    return cf * e**((-1) * ir * period)


def createCashFlows(start_date, freq, tenor, cpn, par):
    num_cfs = (1 / freq) * tenor
    days_from_issue = [int((365 * freq)*(i+1)) for i in range(int(num_cfs))]
    dates = [start_date + datetime.timedelta(i) for i in days_from_issue]
    cfs = [(dates[i], cpn * par * freq) for i in range(len(dates))]
    cfs[-1] = (cfs[-1][0], cfs[-1][-1] + par)
    return cfs

def calcYieldToDate(price, par, tenor, cpn, freq=0.5, guess=None, start_date=datetime.datetime.today()):
    freq = float(freq)
    # guess ytm = coupon rate, will get us in the ball park
    guess = cpn / par
    cfs = createCashFlows(start_date, freq, tenor, cpn, par)
    # convert cpn from annual rate to actual coupon
    coupon = cpn * freq
    dts = [(i[0] - datetime.datetime.today()).days / 365 for i in cfs]
    ytm_func = lambda y: \
        sum([coupon/(1+y*freq)**(t/freq) for t in dts]) + \
        par/(1+y*freq)**(tenor/freq) - price
        
    return optimize.newton(ytm_func, guess)
    
    
if __name__ == "__main__":
    # import pdb; pdb.set_trace()
    # print(bootstrap(0.048, 400, [(0.053, 91), (0.055, 98)]))
    # print(calcYieldToDate(95.0428, 100, 1.5, 5.75))
    print(calcYieldToDate(100, 100, 2, 6))