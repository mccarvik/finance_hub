import sys
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import datetime, pdb
import numpy as np
from app.utils.db_utils import *
from app.equity.screener_eqs.equity_screener import get_data
from app.equity.screener_eqs.equity_stats import EquityStats, ES_Dataframe

RATIOS = ['forwardPE', 'priceToBook', 'priceToSales', 'enterpriseToRevenue',
        'enterpriseToEbitda', 'quickRatio', 'currentRatio', 'debtToEquity', 'returnOnAssets',
        'returnOnEquity']
OTHER_KEY_STATS = ['shortRatio', 'beta', 'beta3Year', 'yield', 'trailingEps', 'forwardEps',
                'pegRatio', 'lastDividendValue', 'currentPrice', 'totalCashPerShare', 
                'revenuePerShare', 'bookValuePerShare', '52WeekChange']
RETURNS = ['ytdReturn', 'threeYearAverageReturn', 'fiveYearAverageReturn']
GROWTH = ['earningsQuarterlyGrowth', 'revenueQuarterlyGrowth', 'earningsGrowth', 'revenueGrowth']
MARGINS = ['profitMargins', 'grossMargins', 'ebitdaMargins', 'operatingMargins']
GROSS_VALUES = ['enterpriseValue', 'totalAssets', 'totalRevenue', 'totalDebt', 'totalCash',
            'ebitda', 'operatingCashflow', 'grossProfits', 'freeCashflow',
            'earningsLow', 'earningsHigh', 'revenueAverage', 'revenueLow', 'revenueHigh',
            'netIncomeToCommon',  'earningsAverage']
            
ANALYSTS = ['morningStarOverallRating', 'morningStarRiskRating','targetMeanPrice', 
            'recommendationMean', 'targetHighPrice', 'targetLowPrice', 'targetMedianPrice',
            'numberOfAnalystOpinions', 'recommendationKey']
DATES = ['exDividendDate', 'dividendDate', 'earningsDate', 'lastSplitDate', 'nextFiscalYearEnd',
        'fundInceptionDate', 'lastFiscalYearEnd', 'mostRecentQuarter']
MISC= ['floatShares', 'sharesOutstanding', 'sharesShort', 'sharesShortPriorMonth',
        'heldPercentInsiders', 'heldPercentInstitutions', 'shortPercentOfFloat', 
        'annualReportExpenseRatio', 'legalType', 'lastSplitFactor', 'SandP52WeekChange',
        'annualHoldingsTurnover', 'maxAge', 'lastCapGain']
CATEGORIES = ['fundFamily', 'category']
COLS_EMPTY_FROM_API = ['priceToSalesTrailing12Months', 'revenueQuarterlyGrowth'
                        'beta3Year', 'yield', 'lastDividendValue', 'ytdReturn'
                        'threeYearAverageReturn', 'fiveYearAverageReturn', 
                        'totalAssets', 'morningStarOverallRating', 'lastCapGain',
                        'morningStarRiskRating', 'fundInceptionDate', 'legalType',
                        'annualReportExpenseRatio', 'annualHoldingsTurnover',
                        'fundFamily', 'category']


def getKeyStatsDataFrame(date=datetime.date.today().strftime('%Y-%m-%d'), tickers=None):
    table = 'key_stats_yahoo'
    where_ticks = "(\""
    for t in tickers:
        where_ticks += t + "\",\""
    where_ticks = where_ticks[:-2] + ")"
    with DBHelper() as db:
        db.connect()
        df = db.select(table, where="date='{0}' and ticker in {1}".format(date, where_ticks)).set_index(['ticker', 'date'])
        df = cleanDF(df)
        return addCustomColumns(df)

def loadDataToDB():
    get_data()
    
def cleanDF(df):
    df = df.apply(pd.to_numeric, errors='ignore')
    df = renameColumns(df)
    return df

def renameColumns(df):
    df = df.rename(index=str, columns={"bookValue": "bookValuePerShare"})
    return df

def addCustomColumns(df):
    df['priceToSales'] = df['currentPrice'] / df['revenuePerShare']
    return df

if __name__ == "__main__":
    loadDataToDB()