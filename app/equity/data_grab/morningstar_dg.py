import sys
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import pandas as pd
import os, csv, requests, asyncio, time, json, io
from threading import Thread
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
    # Remove 2 header lines
    dates = urlData.splitlines()[2]
    lines = urlData.splitlines()[3:]
    data = pd.DataFrame([l.split(",") for l in lines])
    data = pruneData(data, dates)
    return data
    
    
    

def pruneData(df, dates):
    import pdb; pdb.set_trace()
    df['header'] = df.apply(lambda x: ms_dg_helper.COL_MAP[x[0].strip()])
    df['header'] = df.apply(lambda x: x)
    df = df.transpose()
    return df


if __name__ == "__main__":
    getData()