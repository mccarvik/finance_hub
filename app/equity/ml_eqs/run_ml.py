import sys
sys.path.append("/home/ubuntu/workspace/finance")
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import datetime, pdb, time
import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from app import app
from app.equity.screener_eqs.equity_screener import get_data
from app.equity.screener_eqs.equity_stats import EquityStats, ES_Dataframe
from app.equity.analysis_eqs.utils_analysis import loadDataToDB, getKeyStatsDataFrame
from app.equity.data_grab import ms_dg_helper
from app.utils.db_utils import DBHelper
from app.equity.ml_eqs.perceptron import Perceptron
from app.equity.ml_eqs.adalinegd import AdalineGD
from app.equity.ml_eqs.ml_utils import plot_decision_regions

IMG_PATH = '/home/ubuntu/workspace/finance/app/static/img/ml_imgs/'

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
    df = addTarget(df)
    df = cleanData(df)
    df = selectInputs(df, inputs)

    # Run Perceptron
    # run_perceptron(df)
    run_adalinegd(df)


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
    df['target'] = df.apply(lambda x: targetToCat(x['target_proxy']), axis=1)
    return df

def targetToCat(x):
    if (x > 10):
        return 1
    else:
        return -1

def removeUnnecessaryColumns(df):
    df = df[ms_dg_helper.RATIOS + ms_dg_helper.KEY_STATS + ms_dg_helper.OTHER +
            ms_dg_helper.GROWTH + ms_dg_helper.MARGINS + ms_dg_helper.RETURNS +
            ms_dg_helper.PER_SHARE + ms_dg_helper.INDEX]
    return df

def cleanData(df):
    df = df[df['trailingPE'] != 0]
    df = df[df['priceToBook'] > 0]
    df = df[df['priceToSales'] != 0]
    df = df[df['divYield'] >= 0]
    
    # Temp for training purposes
    df = df[abs(df['trailingPE']) < 200]
    df = df[abs(df['priceToBook']) < 10]
    df = df[df['trailingPE'] > 0]
    return df

def run_perceptron(df, eta=0.1, n_iter=10):
    ''' Takes the pruned dataframe and runs it through the perceptron class
    
        Parameters
        ==========
        df : dataframe
            dataframe with the inputs and target
        eta : float
            learning rate between 0 and 1
        n_iter : int
            passes over the training dataset
        
        Return
        ======
        NONE
    '''
    t0 = time.time()
    y = df['target']
    X = df[['divYield','priceToBook']]
    buy = df[df['target'] > 0][list(X.columns)].values
    sell = df[df['target'] < 0][list(X.columns)].values
    plt.figure(figsize=(7,4))
    plt.scatter(buy[:, 0], buy[:, 1], color='blue', marker='x', label='Buy')
    plt.scatter(sell[:, 0], sell[:, 1], color='red', marker='s', label='Sell')
    plt.xlabel(list(X.columns)[0])
    plt.ylabel(list(X.columns)[1])
    plt.legend()
    ppn = Perceptron(eta, n_iter)
    ppn.fit(X.values, y.values)
    # pdb.set_trace()
    plot_decision_regions(X.values, y.values, classifier=ppn)
    plt.savefig(IMG_PATH + "scatter.png")
    plt.close()
    
    plt.plot(range(1,len(ppn.errors_) + 1), ppn.errors_,marker='o')
    plt.xlabel('Iterations')
    plt.ylabel('Number of misclassifications')
    plt.savefig(IMG_PATH + "misclassifications.png")
    plt.close()
    
    t1 = time.time()
    app.logger.info("Done training data and creating charts, took {0} seconds".format(t1-t0))
    print("Done training data and creating charts, took {0} seconds".format(t1-t0))
    
def run_adalinegd(df, eta=0.1, n_iter=10):
    t0 = time.time()
    y = df['target']
    X = df[['divYield','priceToBook']]
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(8, 4))
    ada1 = AdalineGD(n_iter=10, eta=0.01).fit(X, y)
    ax[0].plot(range(1, len(ada1.cost_) + 1), np.log10(ada1.cost_), marker='o')
    ax[0].set_xlabel('Epochs')
    ax[0].set_ylabel('log(Sum-squared-error)')
    ax[0].set_title('Adaline - Learning rate 0.01')
    
    ada2 = AdalineGD(n_iter=10, eta=0.0001).fit(X, y)
    ax[1].plot(range(1, len(ada2.cost_) + 1), ada2.cost_, marker='o')
    ax[1].set_xlabel('Epochs')
    ax[1].set_ylabel('Sum-squared-error')
    ax[1].set_title('Adaline - Learning rate 0.0001')
    
    plt.tight_layout()
    plt.savefig(IMG_PATH + "adaline_1.png", dpi=300)
    plt.close()
    # plt.show()
    



if __name__ == "__main__":
    run(['trailingPE', 'priceToBook', 'priceToSales', 'divYield'])