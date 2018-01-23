import sys
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
sys.path.append("/usr/local/lib/python3.4/dist-packages")
from app.equity.screener_eqs.create_symbols import create_symbols
from app.equity.screener_eqs.equity_stats import EquityStats, ES_Dataframe
import os, csv, requests, asyncio, time, json
import pandas as pd
from threading import Thread
from app import app

def post(request):
    if request.form['action'] == 'run_screening':
        t_filts = dict(eval(request.form['filters']))['filts']
        ES = run_screening(filters=t_filts, sim=False)
        return [list(ES._colmap.keys())] + [list(ES._colmap.values())] + ES._df.values.tolist()
    
    if request.form['action'] == 'get_data':
        get_data(source="API2")
        writeScreenInfo(source="API2")
        return


def get_data(source="API2"):
    import pdb
    pdb.set_trace()
    tasks = []
    EquityStats.setColumns(source)

    # Get tickers and break them up in efficient manner to get data
    with open("/home/ubuntu/workspace/finance/app/equity/screener_eqs/memb_list_abbrev.txt", "r") as f:
        ct = 0
        tickers = ""
        for line in f:
            tickers += line.strip() + "+"
            ct += 1
            if ct == 20:
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
        for t in tasks:
            if source == "API1":
                threads.append(Thread(target=makeAPICall, args=(t,source,)))
            elif source == "API2":
                threads.append(Thread(target=makeScrapeAPICall, args=(t,source,)))
        [t.start() for t in threads]
        [t.join() for t in threads]
        
        # for running single threaded
        # for t in tasks:
        #     if source == "API1":
        #         makeAPICall(t, source)
        #     elif source == "API2":
        #         makeScrapeAPICall(t, source)
    except Exception as e:
        import pdb; pdb.set_trace()
        exc_type, exc_obj, exc_tb = sys.exc_info()
        app.logger.info("Error in async loop: {0}, {1}, {2}".format(exc_type, exc_tb.tb_lineno, exc_obj))
    t1 = time.time()
    app.logger.info("Done Retrieving data, took {0} seconds".format(t1-t0))
    

def makeAPICall(tickers, source):
    # import pdb; pdb.set_trace()
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
            eqs.append(es)
        except Exception as e:
            import pdb; pdb.set_trace()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            app.logger.info("API GRAB ERROR: {0}, {1}, {2}".format(exc_type, exc_tb.tb_lineno, exc_obj))
    app.logger.info("finished {0}".format(tickers))
    return eqs

def makeScrapeAPICall(tickers, source):
    col_list = list(EquityStats.cols.keys())
    cols = "".join(col_list)
    url = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/$$$$?formatted=true&crumb=T7kld941Rnm&lang=en-US&region=US&modules=defaultKeyStatistics%2CfinancialData%2CcalendarEvents&corsDomain=finance.yahoo.com"

    eqs = []
    for ticker in tickers.split("+"):
        try:
            u = url.replace('$$$$', ticker)
            data = requests.get(u).json()['quoteSummary']['result'][0]
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            app.logger.info("API READ ERROR on {3}: {0}, {1}, {2}".format(exc_type, exc_tb.tb_lineno, exc_obj, ticker))
            continue
        
        scraped_data = {}
        for main_key in data.keys():
            try:
                scraped_data = scrapedAPIHelperRecursive(scraped_data, data, main_key)
            except:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                app.logger.info("API SCRAPE ERROR: {0}, {1}, {2}".format(exc_type, exc_tb.tb_lineno, exc_obj))
        try:
            scraped_data['ticker'] = ticker
            es = EquityStats(scraped_data, col_list, source, write=True)
            eqs.append(es)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            app.logger.info("API LOAD ERROR: {0}, {1}, {2}".format(exc_type, exc_tb.tb_lineno, exc_obj))
            
    app.logger.info("finished {0}".format(tickers))
    return eqs
    

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
                # app.logger.info("data is fucked or empty, setting the val to an empty string {0}".format(key))
                scraped_data[key] = ""
        except:
            print("SUM TING WONG")
    return scraped_data


def writeScreenInfo(source,favorites=True):
    if favorites:
        if source == "API1":
            file = "/home/ubuntu/workspace/finance/app/equity_screener/yahoo_api1_notes.txt"
        elif source == "API2":
            file = "/home/ubuntu/workspace/finance/app/equity_screener/yahoo_api2_notes.txt"
        fav = False
        with open(file, "r") as f:
            for line in f:
                if fav:
                    wr = line.strip()
                    desc = f.readline().strip()
                    break
                if line.strip() == 'favorites':
                    fav = True
        file_screen_info = "/home/ubuntu/workspace/finance/app/equity/screener_eqs/screen_info.csv"
        with open(file_screen_info, 'w') as f:
            f.write("cols,"+wr)
            f.write("\n")
            f.write("desc,"+desc)
    else:
        #TODO need to do something to get all columns and not just favorites
        pass
    app.logger.info("Static info written")
    
def run_screening(filters=None, sim=False):
    # Go thru the file, read each ticker and try to collect data
    print("RUN SCREENING")
    # set each val to a float
    filters = [[x[0],x[1],float(x[2])] for x in filters]
    df = ES_Dataframe(filters=filters)
    return df


if __name__ == '__main__':
    # run_screening(sim=True)
    get_data(source='API1')
    # writeScreenInfo(source="API2")