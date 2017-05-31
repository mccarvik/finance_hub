import sys
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import matplotlib as mpl
mpl.use('Agg')
import datetime, pdb
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from config import IMG_PATH
from app.equity.analysis_eqs import utils_analysis
from app.equity.data_grab import ms_dg_helper
from app.utils import mpl_utils

LOCAL_IMG_PATH = '/static' + IMG_PATH.split('static')[1]


def mvg_avgs(ts, tickers, duration, date=datetime.date.today().strftime('%Y-%m-%d')):
    ''' Creates a chart displaying the closing px data and the 50d and 200d 
        moving averages along with SPY as a proxy for the Market
    
        Parameters
        ==========
        ts : dataframe
            The time series data for the given tickers
        tickers : list
            list of strings of the tickers used
        duration : int
            The lenght in year of the data
        date : date
            The given end date of the data
        
        Return
        ======
        png_str : string
            A sting with the location of the new png
    '''
    ts = ts.ix[3]
    mv_avg_50 = ts[ts.columns[0]].rolling(center=False,window=50).mean()
    mv_avg_50.name = mv_avg_50.name + "_50d_mvg"
    mv_avg_200 = ts[ts.columns[0]].rolling(center=False,window=200).mean()
    mv_avg_200.name = mv_avg_200.name + "_200d_mvg"
    dates = ts.index.values
    plots = [ts[ts.columns[0]], mv_avg_50, mv_avg_200]
    index = ts[ts.columns[-1]]
    
    plt.figure(figsize=(7,4))
    fig, ax1 = plt.subplots()
    col_ct = 0
    for pl in plots:
        ax1.plot(dates, pl.values, mpl_utils.COLORS[col_ct], lw=1.5, label=pl.name)
        col_ct+=1
    # plt.plot(dates, plots[0].values, label='test')
    ax1.axis('tight')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')
    ax1.grid(True)
    
    # # Key line below - get a second plot that shares the x axis
    ax2 = ax1.twinx()
    ax2.plot(dates, index, mpl_utils.COLORS[col_ct], lw=1.5, label="SnP")
    # to add it to the legend
    ax1.plot(0,0, mpl_utils.COLORS[col_ct], label="SnP(R)")
    ax1.legend(loc=0)
    ax2.set_ylabel('Index Level')
    plt.title('Moving Averages')
    plt.savefig(IMG_PATH + 'mvg_avgs', dpi=300)
    plt.close()
    return(LOCAL_IMG_PATH + "mvg_avgs.png")

def price_ratios(ts, ms_df, tickers, date=datetime.date.today().strftime('%Y-%m-%d')):
    ''' Creates a chart displaying the closing px data and the 50d and 200d 
        moving averages along with SPY as a proxy for the Market
    
        Parameters
        ==========
        ts : dataframe
            The time series data for the given tickers
        ms_df : dataframe
            morningstar financials data
        tickers : list
            list of strings of the tickers used
        date : date
            The given end date of the data
        
        Return
        ======
        png_str : string
            A sting with the location of the new png
    '''
    col_map = ms_dg_helper.KEY_STATS + ms_dg_helper.RETURNS + \
            ms_dg_helper.GROWTH + ms_dg_helper.MARGINS + ms_dg_helper.RATIOS + ['date', 'month']
    col_list = [c for c in col_map if c in ms_df.columns]
    ms_df = ms_df[col_list]
    dates = ms_df.apply(lambda x: datetime.date(int(x['date']), int(x['month']), 1), axis=1)
    start_date = ms_df['date'].min() + '-01-01'
    ms_df = ms_df.replace('0', np.nan)
    
    
    plt.figure(figsize=(7,4))
    fig, ax1 = plt.subplots()
    col_ct = 0
    for cat in ['trailingPE', 'priceToBook', 'priceToSales', 'priceToCashFlow']:
        ax1.plot(dates, ms_df[cat].values, mpl_utils.COLORS[col_ct], lw=1.5, label=cat)
        ax1.plot(dates, ms_df[cat].values, mpl_utils.COLORS[col_ct]+mpl_utils.MARKERS[6])
        col_ct+=1
    # plt.plot(dates, plots[0].values, label='test')
    ax1.axis('tight')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Ratio')
    ax1.grid(True)
    
    # # Key line below - get a second plot that shares the x axis
    ax2 = ax1.twinx()
    ts = ts.ix[3].reset_index()
    ax2.plot(ts[ts['Date'] > start_date][ts.columns[0]], ts[ts['Date'] > start_date][ts.columns[1]], mpl_utils.COLORS[col_ct], lw=1.5, label="MSFT(R)")
    # to add it to the legend
    ax1.plot(0,0, mpl_utils.COLORS[col_ct], label="MSFT(R)")
    ax1.legend(loc=0)
    ax2.set_ylabel('Index Level')
    plt.title('Price Ratios - ' + tickers[0])
    plt.savefig(IMG_PATH + 'px_ratios', dpi=300)
    plt.close()
    return(LOCAL_IMG_PATH + "px_ratios.png")
    
def run(tickers, date, cp):
    ''' Central Run / Main method for the chartpacks
    
        Parameters
        ==========
        tickers : list
            list of the tickers used
        date : date
            date to be used in the charts
        cp : string
            tells which set of charts to create
        
        Return
        ======
        pngs : list
            list of pngs to add to the interface
    '''
    ts = utils_analysis.getTS(tickers, date)
    ms_df = utils_analysis.getKeyStatsDataFrame(tickers=tickers, table="morningstar", date="")
    pngs = []
    if cp == "CP1":
        pngs.append(mvg_avgs(ts, tickers, 5, date))
        pngs.append(price_ratios(ts, ms_df, tickers, date))
    return pngs


if __name__ == "__main__":
    run(['MSFT'], "2017-05-24", "CP1")


