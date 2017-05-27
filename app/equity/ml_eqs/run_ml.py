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

def run(inputs, load_data=False):
    if load_data:
        loadDataToDB()
    pdb.set_trace()
    # Getting Dataframe
    df = getKeyStatsDataFrame(table='morningstar', date='')
    df = cleanData(df)
    df = removeUnnecessaryColumns(df)
    pdb.set_trace()
    df = addTarget(df)
    df = selectInputs(df, inputs)


def selectInputs(df, inputs):
    columns = inputs + ['target']
    df = df[inputs]
    return df

def addTarget(df):
    return df

def removeUnnecessaryColumns(df):
    df = df[ms_dg_helper.RATIOS + ms_dg_helper.KEY_STATS + ms_dg_helper.OTHER +
            ms_dg_helper.GROWTH + ms_dg_helper.MARGINS + ms_dg_helper.RETURNS +
            ms_dg_helper.PER_SHARE]
    return df

def cleanData(df):
    df = df[df['trailingPE'] > 0]
    return df

if __name__ == "__main__":
    run(['trailingPE', 'priceToBook', 'priceToSales', 'priceToCashFlow', 'divYield'])