import sys
sys.path.append("/home/ubuntu/workspace/finance")
from app.equity.screener_eqs.create_symbols import create_symbols
import pandas as pd
import os, csv, requests, asyncio, time, json
from threading import Thread
from app import app

def getData():
    # Getting all the tickers from text file
    tasks = []
    with open("/home/ubuntu/workspace/finance/app/equity/screener_eqs/memb_list.txt", "r") as f:
        for line in f:
            tasks.append(line.strip())
    
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
    req = requests.get(url)
    # df = pd.read_csv(req.content.decode('utf-8'))
    content = req.content.decode('utf-8')
    import pdb; pdb.set_trace()
    cr = csv.reader(content.splitlines(), delimiter=',')
    print("")
    



if __name__ == "__main__":
    getData()