import sys
sys.path.append("/home/ubuntu/workspace/finance")
from app.equity_screener.create_symbols import create_symbols
from app.equity_screener.equity_stats import EquityStats, ES_Dataframe
import pandas as pd
import os, csv, requests, asyncio, time
from threading import Thread
from app import app

def post(request):
    if request.form['action'] == 'run_screening':
        # filters = getFilters(req=request)
        filters = getFilters(req)
        run_screening(filters=filters, sim=False)
    
    if request.form['action'] == 'get_data':
        get_data(reset_ticks=False)

def get_data(reset_ticks=False, source="API2"):
    if reset_ticks:
        create_symbols.create_symbols()
    tasks = []
    EquityStats.setColumns(source)
    cwd = os.path.dirname(os.path.realpath(__file__))
    with open(cwd + "/memb_list.txt", "r") as f:
        ct = 0
        tickers = ""
        for line in f:
            tickers += line.strip() + "+"
            ct += 1
            if ct == 10:
                tickers = tickers[:-1]
                tasks.append(tickers)
                tickers = ""
                ct = 0
        else:
            tickers = tickers[:-1]
            tasks.append(tickers)
            
    t0 = time.time()
    threads = []
    try:
        # for running multithreaded: starts the thread and 'joins it' so we will wait for all to finish
        # for t in tasks:
        #     threads.append(Thread(target=makeAPICall, args=(t,source,)))
        # [t.start() for t in threads]
        # [t.join() for t in threads]
        
        # for running single threaded
        for t in tasks:
            if source == "API1":
                makeAPICall(t, source)
            elif source == "API2":
                makeScrapeAPICall(t, source)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        app.logger.info("Error in async loop: {0}, {1}, {2}".format(exc_type, exc_tb.tb_lineno, exc_obj))
    t1 = time.time()
    app.logger.info("Done Retrieving data, took {0} seconds".format(t1-t0))
    

def makeAPICall(tickers, source):
    col_list = list(EquityStats.cols.keys())
    cols = "".join(col_list)
    url = "http://finance.yahoo.com/d/quotes.csv?s=" + tickers + "&f=" + cols
    try:
        req = requests.get(url)
        # app.logger.info("request to {0} successful".format(url))
    except:
        app.logger.info("request to {0} failed".format(url))
        return None
        
    content = req.content.decode('utf-8')
    cr = csv.reader(content.splitlines(), delimiter=',')
    eqs = []
    for row in list(cr):
        try:
            es = EquityStats(row, col_list, source, write=True)
            import pdb; pdb.set_trace()
            sys.exit()
            eqs.append(es)
        except Exception as e:
            sys.exit()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            app.logger.info("API GRAB ERROR: {0}, {1}, {2}".format(exc_type, exc_tb.tb_lineno, exc_obj))
    app.logger.info("finished {0}".format(tickers))
    return eqs

def makeScrapeAPICall(t, source):
    col_list = list(EquityStats.cols.keys())
    cols = "".join(col_list)
    url = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/$$$$?formatted=true&crumb=T7kld941Rnm&lang=en-US&region=US&modules=defaultKeyStatistics%2CfinancialData%2CcalendarEvents&corsDomain=finance.yahoo.com"
    import pdb; pdb.set_trace()
    for ticker in t.split("+"):
        u = url.replace('$$$$', ticker)
        data = requests.get(u).json()['quoteSummary']['result'][0]
        scraped_data = {}
        for main_key in data.keys():
            scraped_data = scrapedAPIHelperRecursive(scraped_data, data, main_key)

def scrapedAPIHelperRecursive(scraped_data, data, key):
    try:
        scraped_data[key] = data[key]['raw']
    except:
        try:
            t_data = data[key]
            if isinstance(t_data, dict) and t_data:
                for key2 in t_data.keys():
                    scraped_data = scrapedAPIHelperRecursive(scraped_data, t_data, key2)
            elif isinstance(t_data, list) and t_data:
                # might need to adjust this
                scraped_data[key] = t_data[0]['raw']
            elif t_data:
                scraped_data[key] = t_data
            else:
                print("data is fucked or empty, setting the val to an empty string {0}".format(key))
                scraped_data[key] = ""
        except:
            print("SUM TING WONG")
    return scraped_data
    
        
def run_screening(filters=None, sim=False):
    # Go thru the file, read each ticker and try to collect data
    print("RUN SCREENING")
    df = ES_Dataframe(filters)

def getFilters(req=None):
    filters = []
    if not req:
        return None

if __name__ == '__main__':
    # import pdb; pdb.set_trace()
    # run_screening(sim=True)
    get_data()