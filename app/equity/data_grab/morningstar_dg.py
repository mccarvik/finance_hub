import sys
sys.path.append("/home/ubuntu/workspace/finance")
from app.equity.screener_eqs.create_symbols import create_symbols
import pandas as pd
import os, csv, requests, asyncio, time, json
from threading import Thread
from app import app

def getData():
    
    # Getting all the tickers
    tasks = []
    with open("/home/ubuntu/workspace/finance/app/equity/screener_eqs/memb_list.txt", "r") as f:
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







if __name__ == "__main__":
    getData()