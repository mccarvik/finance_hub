import sys
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import matplotlib as mpl
mpl.use('Agg')
import datetime, pdb, json, requests, re
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from config import IMG_PATH
from app.utils import mpl_utils
from pandas_datareader.data import Options

def vol_surface(tickers, date):
    print()

def run(tickers, date, cp):
    all_data = getAllOptionData(tickers)
    pngs = []
    if cp == "CP1":
        pngs.append(vol_surface(tickers, date))
    return pngs

def getAllOptionData(tickers):
    # Not implemented for yahoo or google currently
    # Options(tickers[0], 'google').get_all_data()
    url = 'https://www.google.com/finance/option_chain?q=' + tickers[0] + '&output=json'
    data = requests.get(url).content.decode('utf-8')
    data = data.replace("\"", "")
    # Need to reformat JSON as google doesnt return a proper json file
    data = data.replace("+","")
    data = re.subn("\{([A-Za-z0-9_.-]+)\:", r'{"\1":', data)[0]
    data = re.subn("\,([A-Za-z0-9_.-]+)\:", r',"\1":', data)[0]
    data = re.subn("\:([A-Za-z0-9_.-]+)\,", r':"\1",', data)[0]
    data = re.subn("\:([A-Za-z0-9_.-]+)\}", r':"\1"}', data)[0]
    data = re.subn("\:\,", r':"",', data)[0]
    dates = list(set(re.findall("[A-Z][a-z]{2}\s\d{2},\s\d{4}", data)))
    for d in dates:
        data = data.replace(d, '"'+d+'"')
    pdb.set_trace()
    data = json.loads(data)
    exprs = data['expirations']
    return data

if __name__ == "__main__":
    run(['AAPL'], datetime.date.today().strftime('%Y-%m-%d'), "CP1")


