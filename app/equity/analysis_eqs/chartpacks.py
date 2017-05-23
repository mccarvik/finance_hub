import sys
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import matplotlib as mpl
mpl.use('Agg')
import datetime, pdb
import matplotlib.pyplot as plt
from pandas_datareader.data import DataReader
from app.equity.analysis_eqs.utils_analysis import getKeyStatsDataFrame


def mvg_avgs(tickers, duration, date=datetime.date.today()):
    tickers.append('^GSPC')
    pdb.set_trace()
    df = DataReader(tickers, 'yahoo', date - date.timedelta(5), date)
    mv_avg_50 = df[0].rolling(center=False,window=50).mean()
    mv_avg_200 = df[0].rolling(center=False,window=200).mean()
    
    print()
    plt.plot(df['date'], [df[0], df[1], mv_avg_50, mv_avg_200])


def run(tickers, date, cp):
    ms_df = getKeyStatsDataFrame(tickers=tickers, table="morningstar", date="")
    pngs = []
    pdb.set_trace()
    if cp == "CP1":
        pngs.append(mvg_avgs(ticker, 5, date))









