import sys
sys.path.append("/home/ubuntu/workspace/finance")
import datetime, pdb
from app import app
from app.equity.screener_eqs.equity_screener import get_data
from app.equity.screener_eqs.equity_stats import EquityStats, ES_Dataframe

def run(load_data=False):
    if load_data:
        load_data_to_db()
    
    df = ES_Dataframe()
    pdb.set_trace()
    df = addDependentVar(df)

def addDependentVar(df):
    pass
    # df['trigger'] = df 

def load_data_to_db(dt=datetime.date.today()):
    # get_data(reset_ticks=True)
    get_data()


if __name__ == "__main__":
    # pdb.set_trace()
    # load_data_to_db()
    run()