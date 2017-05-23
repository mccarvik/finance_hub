import sys
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import matplotlib as mpl
mpl.use('Agg')
import datetime
from pandas_datareader.data import DataReader
from app.equity.analysis_eqs.utils_analysis import getKeyStatsDataFrame


def mvg_avgs(tickers, duration, date=datetime.date.today()):
    tickers.append('^GSPC')
    market = DataReader(tickers, 'yahoo', sdate, edate,pause=1)['Close']
    df['50DayMvgAvg'] = df.apply(lambda x: mv_avg_50[mv_avg_50['Date'] >= datetime.date(int(x.name[1]), \
                        int(x['month']),1)].iloc[0]['Close'], axis=1)
    df['200DayMvgAvg'] = df.apply(lambda x: mv_avg_50[mv_avg_50['Date'] >= datetime.date(int(x.name[1]), \
                        int(x['month']),1)].iloc[0]['Close'], axis=1)


def run(tickers, date, cp):
    ms_df = getKeyStatsDataFrame(tickers=tickers, table="morningstar")
    pngs = []
    if cp == "CP1":
        png.append(mvg_avgs(ticker, 5, date))









