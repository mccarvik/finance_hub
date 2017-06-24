import sys
sys.path.append("/home/ubuntu/workspace/finance")
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import datetime, pdb, time
import numpy as np
import pandas as pd
from app import app
from app.utils.helper_funcs import timeme
from app.equity.analysis_eqs.utils_analysis import loadDataToDB, getKeyStatsDataFrame
from app.equity.data_grab import ms_dg_helper
from app.utils.db_utils import DBHelper
from app.equity.ml_eqs.ml_algorithms import *


def run(inputs, load_data=False):
    if load_data:
        loadDataToDB()
    # Temp to make testing quicker
    t0 = time.time()
    with DBHelper() as db:
        db.connect()
        df = db.select('morningstar', where = 'date in ("2010", "2015")')
    # Getting Dataframe
    # df = getKeyStatsDataFrame(table='morningstar', date='')
    t1 = time.time()
    app.logger.info("Done Retrieving data, took {0} seconds".format(t1-t0))
    print("Done Retrieving data, took {0} seconds".format(t1-t0))
    df = removeUnnecessaryColumns(df)
    df = timeme(addTarget)(df)
    df = cleanData(df)
    df = selectInputs(df, inputs)
    
    # timeme(logisticRegression)(df, tuple(inputs))
    timeme(run_perceptron)(df)

def selectInputs(df, inputs):
    columns = inputs + ['target'] + ['target_proxy']
    df = df[columns]
    return df

def addTarget(df):
    yr_avg_ret = 5
    target = []
    for ind, row in df.iterrows():
        try:
            t = df[(df['ticker'] == row['ticker']) & (df['date'] == str(int(row['date']) + yr_avg_ret))]['5yrReturn'].iloc[0]
            target.append(t)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            target.append(np.nan)
    df['target_proxy'] = target
    df = df.dropna(subset = ['target_proxy'])
    df = df[df['target_proxy'] != 0]
    # med = df['target_proxy'].median()
    # df['target'] = df.apply(lambda x: targetToCat(x['target_proxy'], med), axis=1)
    breaks = np.percentile(df['target_proxy'], [25, 50, 75])
    df['target'] = df.apply(lambda x: targetToCatMulti(x['target_proxy'], breaks), axis=1)
    return df

def targetToCat(x, median):
    if (x > median):
        return 1
    else:
        return -1

def targetToCatMulti(x, breaks):
    cat = 0
    for b in breaks:
        if x < b:
            return cat
        cat += 1
    return cat

def removeUnnecessaryColumns(df):
    df = df[ms_dg_helper.RATIOS + ms_dg_helper.KEY_STATS + ms_dg_helper.OTHER +
            ms_dg_helper.GROWTH + ms_dg_helper.MARGINS + ms_dg_helper.RETURNS +
            ms_dg_helper.PER_SHARE + ms_dg_helper.INDEX]
    return df

def cleanData(df):
    # To filter out errant data
    df = df[df['trailingPE'] != 0]
    df = df[df['priceToBook'] > 0]
    df = df[df['priceToSales'] != 0]
    df = df[df['divYield'] >= 0]
    
    # Temp for training purposes
    df = df[abs(df['trailingPE']) < 100]
    df = df[abs(df['priceToBook']) < 5]
    df = df[df['trailingPE'] > 0]
    df = df[df['divYield'] > 0]
    df = df[df['debtToEquity'] < 5]
    df = df[df['freeCashFlowPerShare'] > 0]
    # pdb.set_trace()
    return df

if __name__ == "__main__":
    run(['trailingPE', 'priceToBook', 'priceToSales', 'divYield', 'debtToEquity',
        'returnOnEquity', 'netIncomeMargin', 'freeCashFlowPerShare'])