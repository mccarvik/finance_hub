import sys
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.finance as mpf
import pandas as pd
import os, csv, requests, asyncio, time, json, io, datetime
from threading import Thread
from pandas.io.data import DataReader
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
    years = [d.split("-")[0] for d in dates]
    months = [d.split("-")[1] for d in dates[:-1]] + ['TTM']
    df['date'] = years
    df['month'] = months
    df['ticker'] = tick
    df = df.set_index(['ticker', 'date'])
    df = cleanData(df)
    addCustomColumns(df)
    sendToDB(df)
    return df

def cleanData(df):
    df = df.apply(pd.to_numeric, errors='ignore')
    return df

def addCustomColumns(df):
    '''
    'sharpe'
    'Treynor'
    'forwardPE'
    'trailingPE'
    'priceToBook'
    'priceToSales'
    'enterpriseToRevenue'
    'enterpriseToEbitda'
    'pegRatio'
    'shortRatio'
    'beta'
    'yield'
    'trailingEps'
    'forwardEps'
    'currentPrice'
    'totalCashPerShare', 
    'dividendPerShare'
    'revenuePerShare'
    '52WeekChange'
    'ytdReturn'
    'threeYearAverageReturn'
    'fiveYearAverageReturn'
    '52WeekLow'
    '52WeekHigh'
    '50DayMvgAvg'
    '200DayMvgAvg'
    'earningsGrowth'
    'revenueGrowth'
    'earningsGrowth'
    'revenueGrowth'
    'ebitdaMargins'
    'enterpriseValue',
    'ebitda', 
    'grossProfits'
    'netIncomeToCommon'
    '''
    start = (int(df.index.get_level_values('date')[-2]), int(df['month'][0]), 1)
    end = tuple([int(d) for d in datetime.date.today().strftime('%Y-%m-%d').split("-")])
    import pdb; pdb.set_trace()
    quotes = DataReader(df.index.get_level_values('ticker')[0],  'yahoo', datetime.date(start), datetime.date(end))
    quotes = mpf.quotes_historical_yahoo_ohlc(df.index.get_level_values('ticker')[0], start, end)
    # df['cur_px'] = df.apply
    return df
    
def sendToDB(df):
    pass

if __name__ == "__main__":
    getData()