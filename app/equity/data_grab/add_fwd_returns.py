import sys, pdb
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import pandas as pd
import numpy as np
from app.utils.db_utils import DBHelper

def add_fwd_returns():
    with DBHelper() as db:
        db.connect()
        df = db.select('morningstar')
        
    yr_avg_rets = [1, 3, 5, 10]
    yar_map = {
        1 : '1yrReturn',
        3 : '3yrReturn',
        5 : '5yrReturn',
        10 : '10yrReturn',
    }
    
    for yar in yr_avg_rets:
        target = []
        for ind, row in df.iterrows():
            try:
                t = df[(df['ticker'] == row['ticker']) & (df['date'] == str(int(row['date']) + yar))][yar_map[yar]].iloc[0]
                target.append(t)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                target.append(np.nan)
        col_title = str(yar) + "yrFwdReturn"
        df[col_title] = target
        print('finished ' + col_title)
    
    pdb.set_trace()
    df = df[['date', 'ticker', '1yrFwdReturn', '3yrFwdReturn', '5yrFwdReturn', '10yrFwdReturn']]
    sendToDB(df)

def sendToDB(df):
    with DBHelper() as db:
        db.connect()
        table = 'morningstar'
        prim_keys = ['date', 'ticker']
        for ind, vals in df.iterrows():
            val_dict = vals.to_dict()
            db.upsert(table, val_dict, prim_keys)
            

if __name__ == '__main__':
    add_fwd_returns()