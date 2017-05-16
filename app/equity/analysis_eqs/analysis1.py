import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import sys
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import datetime, pdb
import pandas as pd
import numpy as np
from app.equity.analysis_eqs import utils_analysis
from app.utils import mpl_utils

def customfilters(tickers=None):
    df = utils_analysis.getFinalDataFrame('2017-05-15', tickers)
    
    # Pruning DB to numbers I am more focused on
    df = df[utils_analysis.RATIOS + utils_analysis.OTHER_KEY_STATS + 
            utils_analysis.GROWTH + utils_analysis.MARGINS]
    
    pdb.set_trace()
    df = df[df['trailingPE'] <20]
    df = df[df['trailingEps'] > 0]
    df = df[df['yield']>0]

def fundamentalsBar(tickers, date='2017-05-15'):
    df = utils_analysis.getFinalDataFrame(date, tickers)
    df = df[utils_analysis.RATIOS + utils_analysis.OTHER_KEY_STATS + 
            utils_analysis.GROWTH + utils_analysis.MARGINS]
    df = df[['forwardPE', 'yield', 'pegRatio', 'beta', 'priceToBook', 'priceToSales']]
    bar_data = {}
    for t in tickers:
        vals = df.loc[(df.index.get_level_values('date') == date) & 
                (df.index.get_level_values('ticker') == t)].values[0]
        bar_data[t] = vals
    
    n_groups = 6
    # means_men = (20, 35, 30, 35, 27)
    # std_men = (2, 3, 4, 1, 2)

    # means_women = (25, 32, 34, 20, 25)
    # std_women = (3, 5, 2, 3, 3)

    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.9 / len(tickers)
    shift = 0.0
    opacity = 0.4
    error_config = {'ecolor': '0.3'}
    col_ct = 0
    
    for t in tickers:
        rects1 = plt.bar(index + shift, bar_data[t], bar_width,
                 alpha=opacity,
                 color=mpl_utils.COLORS[col_ct],
                 error_kw=error_config,
                 label=t)
        mpl_utils.autolabel(rects1, ax)
        shift += bar_width
        col_ct += 1
        mpl_utils.autolabel(rects1, ax)
        

    plt.xlabel('Ratio')
    plt.ylabel('Value')
    plt.title('Fundamentals')
    plt.xticks(index + bar_width / 2, ('Fwd P/E', 'Div Yld', 'Beta', 'PEG', 'P/B', 'P/S'))
    plt.legend(loc=0)
    plt.tight_layout()
    plt.savefig(utils_analysis.PATH + 'fundamentals_bar.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    # customfilters(['MSFT', 'AAPL'])
    fundamentalsBar(['MSFT', 'AAPL', 'CSCO'])