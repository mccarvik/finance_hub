import sys
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import datetime, pdb
import pandas as pd
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
    df = df


if __name__ == "__main__":
    # customfilters(['MSFT', 'AAPL'])
    customfilters()