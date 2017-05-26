import sys
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import matplotlib as mpl
mpl.use('Agg')
import datetime, pdb, json, requests, re
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from functools import reduce
from mpl_toolkits.mplot3d import Axes3D
from config import IMG_PATH
from app.utils import mpl_utils
from app.options.vanilla.opt_vanilla import OptionVanilla
from app.equity.analysis_eqs.utils_analysis import stringToDate
from pandas_datareader.data import Options

def vol_surface(opts, tickers, date, ot):
    underlying_px = opts['underlying_px'].iloc[0]
    exp = opts.expiry.unique()
    strike = [o['strike'] for o in [opts[opts['expiry'] == e] for e in exp]]
    # strike = [o['strike'] for o in opts if o['opt_type'][0] == ot]
    strike = list(reduce(set.intersection, [set(list(s)) for s in strike]))
    iv = {}
    for e in exp:
        for s in strike:
            # premium = [o['p'].iloc[0] for o in opts[(opts['strike']==s) & (opts['expiry']==e) & (opts['opt_type']==ot)]]
            premium = opts[(opts['strike']==s) & (opts['expiry']==e) & (opts['opt_type']==ot)]['p'].iloc[0]
            tenor = (e - stringToDate(date)).days / 365
            # Assume 2% interest rate and 0 % dividend rate
            c_or_p = 'C' if ot == 'Call' else 'P'
            iv[(e,s)] = OptionVanilla(c_or_p, underlying_px, s, 0.02, tenor, 0, prem=premium[0]).vol
    iv = {k : v for k, v in iv.items() if not np.isnan(v)}
    
    # strike, exp = np.meshgrid(strike, exp)
    fig = plt.figure(figsize=(7,4))
    ax = fig.add_subplot(111, projection='3d')
    # surf = ax.plot_surface([float(x[1]) for x in list(iv.keys())], 
    #             [(x[0]-stringToDate(date)).days for x in list(iv.keys())], list(iv.values()), 
    #             rstride=2, cstride=2, cmap=plt.cm.coolwarm, linewidth=0.5, antialiased=True)
    ax.scatter([float(x[1]) for x in list(iv.keys())], [(x[0]-stringToDate(date)).days for x in list(iv.keys())], 
                list(iv.values()), c="b", marker="o")
    ax.set_xlabel('strike')
    ax.set_ylabel('time-to-maturity')
    ax.set_zlabel('implied volatility')
    plt.title('Volatility Surface - ' + tickers[0] + " (" + ot + "s)")
    # fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.savefig(IMG_PATH + 'vol_surface.png', dpi=300)
    plt.close()
    return IMG_PATH + 'vol_surface.png'

def vol_smile(opts, tickers, date, ot):
    underlying_px = opts['underlying_px'].iloc[0]
    exp = opts.expiry.unique()
    strike = [o['strike'] for o in [opts[opts['expiry'] == e] for e in exp]]
    # strike = [o['strike'] for o in opts if o['opt_type'][0] == ot]
    strike = list(reduce(set.intersection, [set(list(s)) for s in strike]))
    iv = {}
    for e in exp:
        iv_exp = []
        for s in strike:
            # premium = [o['p'].iloc[0] for o in opts[(opts['strike']==s) & (opts['expiry']==e) & (opts['opt_type']==ot)]]
            premium = opts[(opts['strike']==s) & (opts['expiry']==e) & (opts['opt_type']==ot)]['p'].iloc[0]
            tenor = (e - stringToDate(date)).days / 365
            # Assume 2% interest rate and 0 % dividend rate
            c_or_p = 'C' if ot == 'Call' else 'P'
            iv_exp.append((s, OptionVanilla(c_or_p, underlying_px, s, 0.02, tenor, 0, prem=premium[0]).vol))
        
        iv_exp = [i for i in iv_exp if not np.isnan(i[1])]
        iv_exp = sorted(iv_exp, key=lambda tup: tup[0])
        iv[e] = iv_exp
    
    plt.figure(figsize=(7,4))
    fig, ax1 = plt.subplots()
    col_ct = 0
    for e in exp:
        ax1.plot([v[0] for v in iv[e]], [v[1] for v in iv[e]], mpl_utils.COLORS[col_ct], lw=1.5, label=e.strftime('%Y-%m-%d'))
        ax1.plot([v[0] for v in iv[e]], [v[1] for v in iv[e]], mpl_utils.COLORS[col_ct]+mpl_utils.MARKERS[6])
        col_ct+=1
    plt.axvline(x=float(underlying_px), color='r', linestyle='--')
    ax1.plot(np.NaN, np.NaN, "r", label="ATM")
    ax1.axis('tight')
    ax1.set_xlabel('Strike')
    ax1.set_ylabel('Implied Volatility')
    ax1.grid(True)
    
    ax1.legend(loc=0)
    ax1.autoscale_view(True,True,True)
    plt.title('Volatility Smile by Expiry - ' + tickers[0] + " (" + ot + "s)")
    # fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.savefig(IMG_PATH + 'vol_smile_exp.png', dpi=300)
    plt.close()
    return IMG_PATH + 'vol_smile_exp.png'
    
    

def run(tickers, date, cp):
    all_data = getAllOptionData(tickers)
    pngs = []
    if cp == "CP1":
        # pngs.append(vol_surface(all_data, tickers, date, 'Call'))
        pngs.append(vol_smile(all_data, tickers, date, 'Call'))
    return pngs

def getAllOptionData(tickers):
    # Not implemented for yahoo or google currently
    # Options(tickers[0], 'google').get_all_data()
    url = 'https://www.google.com/finance/option_chain?q=' + tickers[0] + '&output=json'
    data = requests.get(url).content.decode('utf-8')
    data = cleanGoogleJSON(data)
    underlying_px = data['underlying_price']
    expiry = data['expiry']
    expirations = data['expirations'][1:]
    data = {key: value for key, value in data.items() 
             if key in ['calls', 'puts']}
    options = addColumns(pd.DataFrame(data['calls']), 'Call', expiry, underlying_px)
    options = options.append(addColumns(pd.DataFrame(data['puts']), 'Put', expiry, underlying_px))
    for exp in expirations:
        url = 'https://www.google.com/finance/option_chain?q=' + tickers[0] + '&expd=' + exp['d'] + '&expm=' + exp['m'] + '&expy=' + exp['y'] + '&output=json'
        data = requests.get(url).content.decode('utf-8')
        data = cleanGoogleJSON(data)
        data = {key: value for key, value in data.items() 
             if key in ['calls', 'puts']}
        options = options.append(addColumns(pd.DataFrame(data['calls']), 'Call', exp, underlying_px))
        options = options.append(addColumns(pd.DataFrame(data['puts']), 'Put', exp, underlying_px))
    return options

def addColumns(df, opt_type, expiry, und_px):
    df['expiry'] = datetime.date(int(expiry['y']), int(expiry['m']), int(expiry['d']))
    df['opt_type'] = opt_type
    df['underlying_px'] = und_px
    # df.set_index()????
    return df

def cleanGoogleJSON(data):
    data = data.replace("\"", "")
    # Need to reformat JSON as google doesnt return a proper json file
    data = data.replace("+","")
    data = re.subn("\{([A-Za-z0-9_.-]+)\:", r'{"\1":', data)[0]
    data = re.subn("\,([A-Za-z0-9_.-]+)\:", r',"\1":', data)[0]
    data = re.subn("\:([A-Za-z0-9_.-]+)\,", r':"\1",', data)[0]
    data = re.subn("\:([A-Za-z0-9_.-]+)\}", r':"\1"}', data)[0]
    data = re.subn("\:\,", r':"",', data)[0]
    dates = list(set(re.findall("[A-Z][a-z]{2}\s\d{2},\s\d{4}", data)))
    for d in dates:
        data = data.replace(d, '"'+d+'"')
    return json.loads(data)

if __name__ == "__main__":
    run(['AAPL'], datetime.date.today().strftime('%Y-%m-%d'), "CP1")


