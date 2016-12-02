import datetime
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

def calcYieldToDate(end_date):
    pass
        
    
    
if __name__ == "__main__":
    # import pdb; pdb.set_trace()
    print(bootstrap(0.048, 400, [(0.053, 91), (0.055, 98)]))