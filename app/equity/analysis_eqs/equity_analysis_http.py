import sys
sys.path.append("/home/ubuntu/workspace/finance")
import pandas as pd
import os, csv, requests, asyncio, time, json
from app import app
from app.equity.analysis_eqs import utils_analysis

def post(request):
    if request.form['action'] == 'get_data':
        print("Loading data to DB")
        app.logger.info("Retrieving Data from api, called from")
        utils_analysis.loadDataToDB()
    
    if request.form['action'] == 'generate_charts':
        pass

    return
