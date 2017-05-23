import sys
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import matplotlib as mpl
mpl.use('Agg')
import datetime, pdb
import matplotlib.pyplot as plt
from pandas_datareader.data import DataReader
from config import IMG_PATH
from app.equity.analysis_eqs.utils_analysis import getKeyStatsDataFrame, stringToDate
from app.equity.data_grab import ms_dg_helper
from app.utils import mpl_utils



def mvg_avgs(tickers, duration, date=datetime.date.today().strftime('%Y-%m-%d')):
    date = stringToDate(date)
    tickers.append('SPY')
    df = DataReader(tickers, 'google', date - datetime.timedelta(duration*365), date)
    df = df.ix[3]
    mv_avg_50 = df[df.columns[0]].rolling(center=False,window=50).mean()
    mv_avg_50.name = mv_avg_50.name + "_50d_mvg"
    mv_avg_200 = df[df.columns[0]].rolling(center=False,window=200).mean()
    mv_avg_200.name = mv_avg_200.name + "_200d_mvg"
    dates = df.index.values
    plots = [df[df.columns[0]], mv_avg_50, mv_avg_200]
    index = df[df.columns[-1]]
    
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
    return(IMG_PATH + "mvg_avgs.png")

def price_ratios(ms_df, tickers, date=datetime.date.today().strftime('%Y-%m-%d')):
    col_map = ms_dg_helper.KEY_STATS + ms_dg_helper.RETURNS + \
            ms_dg_helper.GROWTH + ms_dg_helper.MARGINS + ms_dg_helper.RATIOS + ['revenue']
    col_list = [c for c in col_map if c in ms_df.columns]
    ms_df = ms_df[col_list]
    pdb.set_trace()
    print()

def run(tickers, date, cp):
    ms_df = getKeyStatsDataFrame(tickers=tickers, table="morningstar", date="")
    pngs = []
    if cp == "CP1":
        # pngs.append(mvg_avgs(tickers, 5, date))
        pngs.append(price_ratios(ms_df, tickers, date))
    return pngs


if __name__ == "__main__":
    run(['MSFT'], "", "CP1")


