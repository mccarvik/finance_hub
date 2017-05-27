import sys
sys.path.append("/home/ubuntu/workspace/finance")
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import datetime, pdb
import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from app import app
from app.equity.screener_eqs.equity_screener import get_data
from app.equity.screener_eqs.equity_stats import EquityStats, ES_Dataframe
from app.equity.analysis_eqs.utils_analysis import loadDataToDB, getKeyStatsDataFrame
from app.equity.data_grab import ms_dg_helper
from app.utils.db_utils import DBHelper

def run(inputs, load_data=False):
    if load_data:
        loadDataToDB()
    # Temp to make testing quicker
    with DBHelper() as db:
        db.connect()
        df = db.select('morningstar', where = 'date in ("2010", "2013")')
    # Getting Dataframe
    # df = getKeyStatsDataFrame(table='morningstar', date='')
    df = removeUnnecessaryColumns(df)
    df = addTarget(df)
    df = cleanData(df)
    df = selectInputs(df, inputs)

def selectInputs(df, inputs):
    columns = inputs + ['target']
    df = df[inputs]
    return df

def addTarget(df):
    yr_avg_ret = 3
    target = []
    for ind, row in df.iterrows():
        try:
            t = df[(df['ticker'] == row['ticker']) & (df['date'] == str(int(row['date']) + yr_avg_ret))]['3yrReturn'].iloc[0]
            # pdb.set_trace()
            target.append(t)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            target.append(np.nan)
    df['target'] = target
    df = df.dropna(subset = ['target'])
    df = df[df['target'] != 0]
    pdb.set_trace()
    df['target'] = df.apply(lambda x: targetToCat(x['target']), axis=1)
    return df

def targetToCat(x):
    if (x > .1):
        return 2
    elif (x > 0):
        return 1
    else:
        return 0

def removeUnnecessaryColumns(df):
    df = df[ms_dg_helper.RATIOS + ms_dg_helper.KEY_STATS + ms_dg_helper.OTHER +
            ms_dg_helper.GROWTH + ms_dg_helper.MARGINS + ms_dg_helper.RETURNS +
            ms_dg_helper.PER_SHARE + ms_dg_helper.INDEX]
    return df

def cleanData(df):
    df = df[df['trailingPE'] > 0]
    return df

if __name__ == "__main__":
    run(['trailingPE', 'priceToBook', 'priceToSales', 'divYield'])