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

def customfilters(tickers=None):
    df = utils_analysis.getFinalDataFrame('2017-05-15', tickers)
    
    # Pruning DB to numbers I am more focused on
    df = df[utils_analysis.RATIOS + utils_analysis.OTHER_KEY_STATS + 
            utils_analysis.GROWTH + utils_analysis.MARGINS]
    
    pdb.set_trace()
    df = df[df['trailingPE'] <20]
    df = df[df['trailingEps'] > 0]
    df = df[df['yield']>0]

def fundamentalsHist(tickers):
    df = utils_analysis.getFinalDataFrame('2017-05-15', tickers)
    df = df[utils_analysis.RATIOS + utils_analysis.OTHER_KEY_STATS + 
            utils_analysis.GROWTH + utils_analysis.MARGINS]
    df = df[['forwardPE', 'yield', 'pegRatio', 'beta', 'priceToBook', 'priceToSales']]
    pdb.set_trace()
    n_groups = 6
    means_men = (20, 35, 30, 35, 27)
    std_men = (2, 3, 4, 1, 2)

    means_women = (25, 32, 34, 20, 25)
    std_women = (3, 5, 2, 3, 3)

    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.35

    opacity = 0.4
    error_config = {'ecolor': '0.3'}

    rects1 = plt.bar(index, means_men, bar_width,
                 alpha=opacity,
                 color='b',
                 yerr=std_men,
                 error_kw=error_config,
                 label='Men')

    rects2 = plt.bar(index + bar_width, means_women, bar_width,
                 alpha=opacity,
                 color='r',
                 yerr=std_women,
                 error_kw=error_config,
                 label='Women')

    plt.xlabel('Group')
    plt.ylabel('Scores')
    plt.title('Scores by group and gender')
    plt.xticks(index + bar_width / 2, ('Fwd P/E', 'Div Yld', 'PEG', 'P/B', 'P/S'))
    plt.legend(loc=0)
    plt.tight_layout()
    plt.savefig(utils_analysis.PATH + 'fundamentals_bar.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    # customfilters(['MSFT', 'AAPL'])
    fundamentalsHist(['MSFT', 'AAPL'])