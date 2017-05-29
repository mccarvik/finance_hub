import sys
sys.path.append("/home/ubuntu/workspace/finance")
import pandas as pd
import os, csv, requests, asyncio, time, json, pdb
from app import app
from app.equity.analysis_eqs import utils_analysis
from app.equity.analysis_eqs import chartpacks

DEF_RET = json.dumps({'success':True}), 200, {'ContentType':'application/json'}

def post(request):
    
    if request.form['action'] == 'get_data':
        print("Loading data to DB")
        app.logger.info("Retrieving Data from api")
        utils_analysis.loadDataToDB()
        print("Done loading data")
        app.logger.info("Finished retrieving Data from api")
        
    if request.form['action'] == 'gen_charts':
        data = json.loads(request.form['data'])
        tickers = [data['t']]
        pngs = chartpacks.run(tickers, data['d'], data['c'])
        return DEF_RET, pngs
    return DEF_RET

def get(request):
    if request.form['action'] == 'get_data':
        print("Loading data to DB")
        app.logger.info("Retrieving Data from api")
        utils_analysis.loadDataToDB()
        print("Done loading data")
        app.logger.info("Finished retrieving Data from api")
    
    return DEF_RET