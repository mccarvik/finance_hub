import sys
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pdb, datetime, re
from dateutil.relativedelta import relativedelta
from app import app
from config import IMG_PATH
from app.utils import mpl_utils
from app.futures.data_grab.quandl_api_helper import quandl_api_dict, URL, MONTH_MAP
from app.futures.data_grab.quandl_api import callQuandlAPI


def getFuturesCurve(fut, dt=None):
    # urls = getURLs(fut, dt)
    urls = getURLs(fut)
    data = []
    for u in urls:
        try:
            data.append([callQuandlAPI(u[0])['Settle'].iloc[0], u[1]])
        except:
            pat = r'.*?datasets(.*)data.*'
            match = re.search(pat, u[0])
            regex = match.group(1)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            app.logger.info("No contract for this month and fut: {3}  {0}, {1}, {2}".format(exc_type, exc_tb.tb_lineno, exc_obj, regex))

    data = [[datetime.date(int(d[1][:4]), int(d[1][4:]), 1) for d in data], [float(d[0]) for d in data]]
    return data
    
def buildURL(db_code, ds_code, start=None, end=None):
    if not end:
        end = datetime.date.today()
    if not start:
        start = (end - datetime.timedelta(7))
    return URL.format(db_code, ds_code, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))

def getURLs(fut, today=None, end=None):
    if not end:
        end = datetime.date.today() + datetime.timedelta(365)
    urls = []
    date = datetime.date.today()
    while date < end:
        d_str = dateToStringFormat(date)
        db_code = quandl_api_dict[fut][0]
        ds_code = quandl_api_dict[fut][1] + d_str
        urls.append([buildURL(db_code, quandl_api_dict[fut][1] + d_str), str(date.year) + str(date.month)])
        one_mon_rel = relativedelta(months=1)
        date = date + one_mon_rel
    return urls
    
def dateToStringFormat(d):
    return str(MONTH_MAP[d.month]) + str(d.year)

def chartCurve(data):
    plt.figure(figsize=(7,4))
    fig, ax1 = plt.subplots()
    col_ct = 0
    for d in data:
        ax1.plot(d[0][0], d[0][1], mpl_utils.COLORS[col_ct], lw=1.5, label=d[1])
        col_ct+=1
    ax1.axis('tight')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')
    ax1.grid(True)
    ax1.legend(loc=0)
    plt.title('Commodity Curves')
    plt.savefig(IMG_PATH + 'comm_curves', dpi=300)
    plt.close()

if __name__ == '__main__':
    fut = ['corn', 'gold']
    curves = []
    for f in fut:
        curves.append([getFuturesCurve(f), f])
    pdb.set_trace()
    chartCurve(curves)
    
    
    
    