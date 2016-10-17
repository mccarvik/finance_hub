import sys
sys.path.append("/home/ubuntu/workspace/finance")
from app.equity_screener.create_symbols import create_symbols
from app.equity_screener.equity_stats import EquityStats
import pandas as pd
import os
import csv
import requests
import asyncio
from app import app

def post(request):
    if request.form['action'] == 'run_screening':
        # filters = getFilters(req=request)
        filters = getFilters(req=None)
        run_screening(filters=filters, sim=False)
    
    if request.form['action'] == 'get_data':
        get_data(reset_ticks=False)


def get_data(reset_ticks=False):
    if reset_ticks:
        create_symbols.create_symbols()
    
    # Need to make this multi threaded with async
    eqs = []
    EquityStats.setColumns()
    cwd = os.path.dirname(os.path.realpath(__file__))
    with open(cwd + "/memb_list.txt", "r") as f:
        ct = 0
        tickers = ""
        for line in f:
            tickers += line.strip() + "+"
            ct += 1
            if ct == 10:
                tickers = tickers[:-1]
                makeAPICall(tickers)
                app.logger.info("finished {0}".format(tickers))
                tickers = ""
                ct = 0
                #temp
                break


async def makeAPICall(tickers):
    col_list = list(EquityStats.cols.keys())
    cols = "".join(col_list)
    url = "http://finance.yahoo.com/d/quotes.csv?s=" + tickers + "&f=" + cols
    try:
        req = requests.get(url)
        app.logger.info("request to {0} successful".format(url))
    except:
        app.logger.info("request to {0} failed".format(url))
        return None
    import pdb; pdb.set_trace()
    content = req.content.decode('utf-8')
    cr = csv.reader(content.splitlines(), delimiter=',')
    eqs = []
    for row in list(cr):
        es = EquityStats(row, col_list)
        eqs.append(es)
    return eqs
    
        
    


def run_screening(filters=None, sim=False):
    # Go thru the file, read each ticker and try to collect data
    print("RUN SCREENING")
    if sim:
        filters = getFilters(req=None)
        
    #build dataframe
    arr_2d = []
    for e in eqs:
        lyst = e.key_stats
        arr_2d.append(lyst)
    df = pd.DataFrame(data=arr_2d, columns=EquityStats.cols)
    filters = getFilters(sim)

    print(df.to_string())
    for f in filters:
        print(f)
        try:
            df[f[0]] = df[f[0]].astype(float)
        except Exception as e:
            print(e, " filter not applied")
            continue
        if f[1] == "=":
            df = df[df[f[0]] == f[2]]
        elif f[1] == ">":
            df = df[df[f[0]] > f[2]]
        elif f[1] == "<":
            df = df[df[f[0]] < f[2]]
        print(df.to_string())

def getFilters(req=None):
    filters = []
    # if not sim:
    #     while True:
    #         print("Select satistic:")
    #         [print(i + ",  ", end="") for i in EquityStats.cols]
    #         stat = input()
    #         if not stat:
    #             break
    #         print('Select conditon:')
    #         print('< or >')
    #         condition = input()
    #         print('Select value:')
    #         val = input()
    #         filters.append((stat, condition, val))
    if req:
        pass
    else:
        filters.append(("P/E", "<", 20))
        filters.append(("Beta", "<", 2))
        filters.append(('Div yield', '>', 1))
    return filters

if __name__ == '__main__':
    # run_screening(sim=True)
    get_data()