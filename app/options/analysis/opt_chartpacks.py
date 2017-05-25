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
from config import IMG_PATH
from app.utils import mpl_utils
from app.options.vanilla.opt_vanilla import OptionVanilla
from app.equity.analysis_eqs.utils_analysis import stringToDate
from pandas_datareader.data import Options

def vol_surface(opts, tickers, date, ot):
    underlying_px = opts[0]['underlying_px'][0]
    exp = [o['expiry'].loc[0] for o in opts if o['opt_type'][0] == ot]
    strike = [o['strike'] for o in opts if o['opt_type'][0] == ot]
    strike = list(reduce(set.intersection, [set(list(s)) for s in strike]))
    iv = {}
    for e in exp:
        for s in strike:
            premium = [o[o['strike']==s]['p'].iloc[0] for o in opts if o['expiry'].iloc[0]==e and o['opt_type'][0] == ot]
            tenor = (e - stringToDate(date)).days / 365
            # Assume 2% interest rate and 0 % dividend rate
            pdb.set_trace()
            iv[[e,s]] = OptionVanilla(ot, underlying_px, s, 0.02, tenor, 0, prem=premium[0])
            
    strike, ttm = np.meshgrid(strike, ttm)
    
    
    fig = plt.figure(figsize=(9,6))
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(strike, exp, iv, rstride=2, cstride=2, 
        cmap=plt.cm.coolwarm, linewidth=0.5, antialiased=True)
    ax.set_xlabel('strike')
    ax.set_ylabel('time-to-maturity')
    ax.set_zlabel('implied volatility')
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.savefig(IMG_PATH + 'vol_surface.png', dpi=300)
    plt.close()
    return IMG_PATH + 'vol_surface.png'

def run(tickers, date, cp):
    all_data = getAllOptionData(tickers)
    pngs = []
    if cp == "CP1":
        pngs.append(vol_surface(all_data, tickers, date, 'call'))
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
    options = []
    # Need to add expiry and maybe C/P column to this
    options.append(addColumns(pd.DataFrame(data['calls']), 'call', expiry, underlying_px))
    options.append(addColumns(pd.DataFrame(data['puts']), 'put', expiry, underlying_px))
    for exp in expirations:
        url = 'https://www.google.com/finance/option_chain?q=' + tickers[0] + '&expd=' + exp['d'] + '&expm=' + exp['m'] + '&expy=' + exp['y'] + '&output=json'
        data = requests.get(url).content.decode('utf-8')
        data = cleanGoogleJSON(data)
        data = {key: value for key, value in data.items() 
             if key in ['calls', 'puts']}
        options.append(addColumns(pd.DataFrame(data['calls']), 'call', exp, underlying_px))
        options.append(addColumns(pd.DataFrame(data['puts']), 'put', exp, underlying_px))
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


