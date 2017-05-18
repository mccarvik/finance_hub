import sys
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.finance as mpf
import pandas as pd
import numpy as np
import os, csv, requests, asyncio, time, json, io, datetime
from threading import Thread
from pandas_datareader.data import DataReader
from app import app
from app.equity.screener_eqs.create_symbols import create_symbols
from app.equity.data_grab import ms_dg_helper


def getData():
    # Getting all the tickers from text file
    tasks = []
    with open("/home/ubuntu/workspace/finance/app/equity/screener_eqs/memb_list.txt", "r") as f:
        for line in f:
            tasks.append(line.strip())
    
    t0 = time.time()
    threads = []
    try:
        # for running multithreaded: starts the thread and 'joins it' so we will wait for all to finish
        # for t in tasks:
        #     threads.append(Thread(target=makeAPICall, args=(t,)))
        # [t.start() for t in threads]
        # [t.join() for t in threads]
        
        # for running single threaded
        for t in tasks:
            makeAPICall(t)
            
    except Exception as e:
        import pdb; pdb.set_trace()
        exc_type, exc_obj, exc_tb = sys.exc_info()
        app.logger.info("Error in async loop: {0}, {1}, {2}".format(exc_type, exc_tb.tb_lineno, exc_obj))
    t1 = time.time()
    app.logger.info("Done Retrieving data, took {0} seconds".format(t1-t0))

def makeAPICall(tick):
    url = 'http://financials.morningstar.com/ajax/exportKR2CSV.html?t=' + tick
    urlData = requests.get(url).content.decode('utf-8')
    cr = csv.reader(urlData.splitlines(), delimiter=',')
    data = []
    for row in list(cr):
        data.append(row)
    # Remove dates
    dates = data[2][1:]
    lines = data[3:]
    # Issue here for certain values with a comma in them
    data = pd.DataFrame(data)
    data = pruneData(data, dates, tick)
    return data
    
    
    

def pruneData(df, dates, tick):
    df = df.set_index(0)
    df = df.transpose()
    # rename columns and throw away random extra columns
    df = df.rename(columns=ms_dg_helper.COL_MAP)
    df = df[list(ms_dg_helper.COL_MAP.values())]
    # The TTM data may be off as that last column has different time windows
    years = [d.split("-")[0] for d in dates[:-1]] + [str(datetime.date.today().year)]
    months = [d.split("-")[1] for d in dates[:-1]] + [str(datetime.date.today().month)]
    df['date'] = years
    df['month'] = months
    df['ticker'] = tick
    df = df.set_index(['ticker', 'date'])
    df = cleanData(df)
    addCustomColumns(df)
    sendToDB(df)
    return df

def cleanData(df):
    # Need this for commas
    df = df.apply(lambda x: pd.to_numeric(x.astype(str).str.replace(',',''), errors='ignore'))
    df = df.fillna(0)
    return df

def addCustomColumns(df):
    start = datetime.date(int(df.index.get_level_values('date')[0])-10, int(df['month'][0]), 1)
    end_date_ls = [int(d) for d in datetime.date.today().strftime('%Y-%m-%d').split("-")]
    end = datetime.date(end_date_ls[0], end_date_ls[1], end_date_ls[2])
    import pdb; pdb.set_trace()
    market = DataReader(".INX", 'google', start, end)['Close']
    quotes = DataReader(df.index.get_level_values('ticker')[0], 'google', start, end)['Close']
    quotes['market'] = market
    import pdb; pdb.set_trace()
    qr = quotes.reset_index()
    df = addBasicCustomCols(df, qr)
    df = addGrowthCustomCols(df, qr)
    df = addTimelineCustomCols(df, qr, quotes)
    '''
    Still need to do:
    'enterpriseToEbitda'
    'ebitdaMargins'
    'ebitda',
    'shortRatio'
    
    'Treynor / beta'
    'sortino / downside vol'
    '''
    return df
    
def addTimelineCustomCols(df, qr, quotes):
    mv_avg_50 = quotes.rolling(center=False,window=50).mean().reset_index()
    mv_avg_200 = quotes.rolling(center=False,window=200).mean().reset_index()
    df['50DayMvgAvg'] = df.apply(lambda x: mv_avg_50[mv_avg_50['Date'] >= datetime.date(int(x.name[1]), \
                        int(x['month']),1)].iloc[0]['Close'], axis=1)
    df['200DayMvgAvg'] = df.apply(lambda x: mv_avg_50[mv_avg_50['Date'] >= datetime.date(int(x.name[1]), \
                        int(x['month']),1)].iloc[0]['Close'], axis=1)
    vol_stdev = quotes.rolling(window=252, center=False).std().reset_index()  # using one year window
    df['volatility'] = (df.apply(lambda x: vol_stdev[vol_stdev['Date'] >= datetime.date(int(x.name[1]), \
                        int(x['month']),1)].iloc[0]['Close'], axis=1)) / df['currentPrice']
    import pdb; pdb.set_trace()
    df['sharpeRatio'] = df['1yrReturn'] / df['volatility']
    df['downsideVol'] = downside_vol(df, vol_stdev, qr) / df['currentPrice']
    df['sortinoRatio'] = df['1yrReturn'] / df['downside_vol']
    # df['treynorRatio'] = df['1yrReturn'] / df['beta']
    # Need to loop through and remove all pos st_devs then calc vol for each year window
    
    return df

def beta(df, qr):
    pass
    # http://stackoverflow.com/questions/21515357/python-script-to-calculate-asset-beta-giving-incorrect-result
    # covariance = numpy.cov(a,b)[0][1]
    # variance = numpy.var(a)
    # beta = covariance / variance

def downside_vol(df, vol_stdev, qr):
    qr['change'] = qr['Close'].pct_change(1)
    neg = qr[qr['Close']<0]
    dv = []
    for ind, vals in df.iterrows():
        dv.append(neg[(neg['Date'] >= datetime.date(int(ind[1])-1,int(vals['month']),1)) \
                                    & (qr['Date'] <= datetime.date(int(ind[1]),int(vals['month']),1))]['Close'].std())
    return dv  

def addBasicCustomCols(df, qr):
    df['currentPrice'] = df.apply(lambda x: qr[qr['Date'] >= datetime.date(int(x.name[1]),int(x['month']),1)].iloc[0]['Close'], axis=1)
    df['revenuePerShare'] = df['revenue'] / df['shares']  
    df['dividendPerShare'] = df['dividend'] / df['shares']
    df['divYield'] = df['dividendPerShare'] / df['currentPrice']
    df['trailingPE'] = df['currentPrice'] / df['trailingEPS']
    df['priceToBook'] = df['currentPrice'] / df['bookValuePerShare']
    df['priceToSales'] = df['currentPrice'] / df['revenuePerShare']
    df['grossProfit'] = (1-df['cogs']) * df['revenue']
    df['marketCapital'] = df['shares'] * df['currentPrice']
    df['totalAssets'] = df['bookValuePerShare'] / df['totalEquity']
    df['enterpriseValue'] = df['marketCapital'] + (df['totalLiabilities'] * df['totalAssets']) - (df['cashAndShortTermInv'] * df['totalAssets'])
    df['enterpriseToRevenue'] = df['enterpriseValue'] / df['revenue']
    df['EBT'] = (df['operatingIncome'] - df['netInterestOtherMargin']) * df['totalAssets']
    return df
    
def addGrowthCustomCols(df, qr):
    rev_growth = []; eps_growth = []
    for ind, vals in df.iterrows():
        try:
            last = df.loc[(df.index.get_level_values('date') == str(int(ind[1])-1))]
            if last.empty:
                rev_growth.append(0)
                eps_growth.append(0)
            else:
                rev_growth.append(float((vals['revenue'] / last['revenue'] - 1) * 100))
                eps_growth.append(float((vals['trailingEPS'] / last['trailingEPS'] - 1) * 100))
        except:
            rev_growth.append(0)
            eps_growth.append(0)
    
    df['revenueGrowth'] = rev_growth
    df['epsGrowth'] = eps_growth
    df['pegRatio'] = df['trailingPE'] / df['epsGrowth']
    
    yr1_ret = []; yr3_ret = []; yr5_ret = []; yr10_ret = []; ytd_ret =[]; min52 = []; max52 = []
    for ind, vals in df.iterrows():
        try:
            yr1q = qr[qr['Date'] >= datetime.date(int(ind[1])-1,int(vals['month']),1)].iloc[0]['Close']
            yr1_ret.append(((vals['currentPrice'] / yr1q - 1) * 100))
        except:
            yr1_ret.append(0)
        try:
            yr3q = qr[qr['Date'] >= datetime.date(int(ind[1])-3,int(vals['month']),1)].iloc[0]['Close']
            yr3_ret.append(((vals['currentPrice'] / yr3q - 1) * 100)**(1/3))
        except:
            yr3_ret.append(0)
        try:
            yr5q = qr[qr['Date'] >= datetime.date(int(ind[1])-5,int(vals['month']),1)].iloc[0]['Close']
            yr5_ret.append(((vals['currentPrice'] / yr5q - 1) * 100)**(1/5))
        except:
            yr5_ret.append(0)
        try:
            yr10q = qr[qr['Date'] >= datetime.date(int(ind[1])-10,int(vals['month']),1)].iloc[0]['Close']
            yr10_ret.append(((vals['currentPrice'] / yr10q - 1) * 100)**(1/10))
        except:
            yr10_ret.append(0)
        try:
            yrytd = qr[qr['Date'] >= datetime.date(int(ind[1])-10,1,1)].iloc[0]['Close']
            ytd_ret.append(((vals['currentPrice'] / yrytd - 1) * 100))
        except:
            ytd_ret.append(0)
        try:
            min52.append(min(qr[(qr['Date'] >= datetime.date(int(ind[1])-1,int(vals['month']),1)) & (qr['Date'] <= datetime.date(int(ind[1]),int(vals['month']),1))]['Close']))
            max52.append(max(qr[(qr['Date'] >= datetime.date(int(ind[1])-1,int(vals['month']),1)) & (qr['Date'] <= datetime.date(int(ind[1]),int(vals['month']),1))]['Close']))
        except:
            min52.append(0)
            max52.append(0)

    df['ytdReturn'] = ytd_ret
    df['1yrReturn'] = yr1_ret
    df['3yrReturn'] = yr3_ret
    df['5yrReturn'] = yr5_ret
    df['10yrReturn'] = yr10_ret
    df['52WeekLow'] = min52
    df['52WeekHigh'] = max52
    return df
    

def getFirstofMonth():
    pass
    
def sendToDB(df):
    pass

if __name__ == "__main__":
    getData()