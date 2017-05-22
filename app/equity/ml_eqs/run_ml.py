import sys
sys.path.append("/home/ubuntu/workspace/finance")
import datetime, pdb
from app import app
from app.equity.screener_eqs.equity_screener import get_data
from app.equity.screener_eqs.equity_stats import EquityStats, ES_Dataframe
from app.equity.analysis_eqs.utils_analysis import loadDataToDB, getKeyStatsDataFrame

def run(load_data=False):
    if load_data:
        loadDataToDB()
    pdb.set_trace()
    df = getKeyStatsDataFrame(table='morningstar', date='')    

def addDependentVar(df):
    pass

if __name__ == "__main__":
    run()