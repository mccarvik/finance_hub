import sys
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import datetime, pdb
import numpy as np
from app.utils.db_utils import *
from app.equity.screener_eqs.equity_screener import get_data
from app.equity.screener_eqs.equity_stats import EquityStats, ES_Dataframe

PATH = '/workspace/finance/app/static/img'
RATIOS = ['forwardPE', 'trailingPE', 'priceToBook', 'priceToSales', 'enterpriseToRevenue',
        'enterpriseToEbitda', 'quickRatio', 'currentRatio', 'debtToEquity', 'returnOnAssets',
        'returnOnEquity', 'pegRatio',]
OTHER_KEY_STATS = ['shortRatio', 'beta', 'beta3Year', 'yield', 'trailingEps', 'forwardEps',
                'lastDividendValue', 'currentPrice', 'totalCashPerShare', 
                'dividendPerShare', 'revenuePerShare', 'bookValuePerShare', '52WeekChange']
RETURNS = ['ytdReturn', 'threeYearAverageReturn', 'fiveYearAverageReturn', '52WeekLow',
            '52WeekHigh', '50DayMvgAvg', '200DayMvgAvg']
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

def getFinalDataFrame(date=datetime.date.today().strftime('%Y-%m-%d'), tickers=None):
    df = getKeyStatsDataFrame(date, tickers)
    df = cleanDF(df, date, tickers)
    return df
    

def getKeyStatsDataFrame(date=datetime.date.today().strftime('%Y-%m-%d'), tickers=None, table='key_stats_yahoo'):    
    ''' Will retrieve the key financial stats from the DB for a given day and tickers
        Will also clean the dataframe data and add any custom columns
    Parameters
    ==========
    date : date
        Date of values retrieved
        DEFAULT = Today
    tickers : list of strings
        list of tickers to be grabbed
        DEFAULT = NONE, will grab everything for given day
    table : string
        The table we are pulling from
        DEFAULT = key_stats_yahoo
    
    Return
    ======
    df : dataframe
        The stats for the given day and tickers
    '''
    where_ticks = "(\""
    if tickers:
        for t in tickers:
            where_ticks += t + "\",\""
    where_ticks = where_ticks[:-2] + ")"
    with DBHelper() as db:
        db.connect()
        if tickers:
            df = db.select(table, where="date='{0}' and ticker in {1}".format(date, where_ticks))
        else:
            df = db.select(table, where="date='{0}'".format(date))
    return df

def loadDataToDB():
    ''' Loads the data from the APIs into the DB
    Parameters
    ==========
    NONE
    
    Return
    ======
    NONE
    '''
    get_data()
    # Need this to load data from the other API
    get_data(source='API1')

def cleanDF(df, date, tickers):
    ''' Cleans the dataframe, numberfy certain columns, rename columns, etc
    Parameters
    ==========
    df : dataframe
        df to be cleaned

    Return
    ======
    df : dataframe
        The cleaned dataframe
    '''
    df = df.set_index(['ticker', 'date'])
    df = df.apply(pd.to_numeric, errors='ignore')
    df = renameColumns(df)
    df = addOtherAPIColumns(df, date, tickers)
    df = addCustomColumns(df)
    # removes all without a price
    df = df[np.isfinite(df['currentPrice'])]
    df = df[df['currentPrice'] > 0]
    return df

def renameColumns(df):
    ''' Renamed specifed columns
    Parameters
    ==========
    df : dataframe
        the dataframe to have columns renamed
    
    Return
    ======
    df : dataframe
        the dataframe with columns to be renamed
    '''
    df = df.rename(index=str, columns={"bookValue": "bookValuePerShare"})
    return df

def addOtherAPIColumns(df, date, tickers):
    '''Will retrive selected columns from other API, most notably div_yield
    Parameters
    ==========
    df : dataframe
        df to be augmented

    Return
    ======
    df : dataframe
        The augmented dataframe
    '''
    additional_cols = ['dividendPerShare', '52WeekLow', '52WeekHigh', '50DayMvgAvg', '200DayMvgAvg']
    df_new = getKeyStatsDataFrame(date, tickers, table='eq_screener')
    df_new = df_new.set_index(['ticker', 'date'])
    df_new = df_new.rename(index=str, columns={"d":"dividendPerShare", "j":"52WeekLow",
            "k":"52WeekHigh", "m3":"50DayMvgAvg", "m4":"200DayMvgAvg", "y":"yield"})
    df_new['yield'] = df_new['yield'].replace('N/A', 0)
    df_new = df_new.apply(pd.to_numeric, errors='ignore')
    df_yld = pd.DataFrame(df_new['yield'])
    df_new = df_new[additional_cols]
    df = pd.concat([df, df_new], axis=1)
    df['yield'] = df_yld['yield']
    return df

def addCustomColumns(df):
    ''' Creating columns to add to the dataframe
    Parameters
    ==========
    df : dataframe
        The dataframe to be appended
    
    Return
    ======
    df : dataframe
        The augmented dataframe
    '''
    df['priceToSales'] = df['currentPrice'] / df['revenuePerShare']
    df['trailingPE'] = df['currentPrice'] / df['trailingEps']
    # will need to calculate volatility for sharpeRatio
    df['treynorRatio']
    df['sharpeRatio']
    return df

if __name__ == "__main__":
    # loadDataToDB()
    pass