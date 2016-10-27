import sys
sys.path.append("/home/ubuntu/workspace/finance")
import datetime
import re, os, string
import pandas as pd
from app import app
from app.utils.db_utils import DBHelper

column_opts = []

class EquityStats():
    """holds all the individual stats for a stock
    like P/E, dividend yield, etc.
    """
    
    def __init__(self, stats, col_list, write=False, date=None):
        self._stats = dict(zip(col_list, stats))
        self._ticker = self._stats['s']
        self._date = date or datetime.datetime.now().strftime('%Y-%m-%d')
        self._stats['date'] = self._date
        if write:
            self.write_to_db()
    
    def write_to_db(self):
        with DBHelper() as db:
            db.connect()
            self._stats['n'] = self._stats['n'].replace("'", "''")
            db.upsert('eq_screener', self._stats, ['date', 's'])
        
    
    @staticmethod
    def setColumns():
        column_map = {}
        with open("/home/ubuntu/workspace/finance/app/equity_screener/yahoo_api_notes.txt", "r") as f:
            for line in f:
                if line.strip() == 'EOF':
                    break
                t_tup = line.split('\t')
                column_map[t_tup[0]] = t_tup[1]
        EquityStats.cols = column_map


class ES_Dataframe:
    """HOlds the dataframe of a call to the eq_screener DB
    and preforms all the filters"""
    
    exempt_list = ['l', 'i', 's', 'n', 'w', 'e1', 'm', 'm2', 'n4', 'x']
    to_numeric_list = ['a', 'a2', 'a5', 'b', 'b2', 'b3', 'b4', 'b6', 'c', 'c1', 'c3', 'c6', 'c8', 'd', 'e',
                        'e7', 'e8', 'e9', 'f6', 'g', 'h', 'j', 'k', 'g1', 'g3', 'g4', 'g5', 'g6', 'j1', 'j3', 
                        'j4', 'j5', 'j6', 'k1', 'k2', 'k3', 'k4', 'k5', 'l1', 'l2', 'l3', 'm3', 'm4', 'm5',
                        'm6', 'm7', 'o', 'p', 'p1', 'p2', 'p5', 'p6', 'r', 'r2', 'r5', 'r6', 'r7', 's1', 's7',
                        't6', 't7', 't8', 'v', 'v1', 'v7', 'w1', 'w4', 'y']
    fav_list = ['a', 'a2', 'a5', 'b', 'b4', 'b6', 'd', 'e', 'e7', 'e8', 'e9', 'f6', 'j', 'k', 'j1', 'j4',
                'j5', 'j6', 'k4', 'k5', 'l1', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'p', 'p5', 'p6', 'r', 'r5'
                'r6', 'r7', 's7', 't8', 'v', 'w1', 'y']
    test_filters = [('r', '<', 20),  ('y', '>', 1)]
    
    def __init__(self, date=None, filters=None, favs=False):
        self._favs = favs
        self._filters = filters or ES_Dataframe.test_filters
        self._colmap = self.setColumns()
        self._date = date or datetime.datetime.now().strftime('%Y-%m-%d')
        self._df = self.read_from_db()
        self.write_static_info()
        self.clean_data()
        self.apply_filters()
    
    def read_from_db(self):
        with DBHelper() as db:
            db.connect()
            return db.select('eq_screener', where="date='{0}'".format(self._date))
        
    @staticmethod
    def setColumns():
        column_map = {}
        with open("/home/ubuntu/workspace/finance/app/equity_screener/yahoo_api_notes.txt", "r") as f:
            for line in f:
                if line.strip() == 'EOF':
                    break
                t_tup = line.split('\t')
                column_map[t_tup[0]] = t_tup[1]
        return column_map
    
    def write_static_info(self):
        # columns that arent conducive to screenng
        cols = list(set(self._colmap.keys()) - set(ES_Dataframe.exempt_list))
        with open('/home/ubuntu/workspace/finance/app/equity_screener/screen_info.csv', 'w') as f:
            f.write("columns," + ",".join(cols) + '\n')
            f.write("favorites," + ",".join(ES_Dataframe.fav_list) + '\n')
        app.logger.info("Static info written")
    
    def clean_data(self):
        """moves around data in the dataframe for screening purposes"""
        self.removePunctuation()
        self.numberfy()
        app.logger.info("Done cleaning data")
    
    def removePunctuation(self):
        """replacing punctiation in all the columns"""
        df = self._df
        for col in df.columns:
            if not isinstance(df[col][0], str):
                continue
            for pct in ['+', '%']:
                try:
                    df[col] = df[col].apply(lambda x: x.replace(pct,""))
                except Exception as e:
                    print("column prob doesnt need punctiation cleaning" + e)
                    # exc_type, exc_obj, exc_tb = sys.exc_info()
                    # app.logger.info("PANDAS DATA CLEAN ERROR: {0}, {1}, {2}".format(exc_type, exc_tb.tb_lineno, exc_obj))
        self._df = df
    
    def numberfy(self):
        """sets all the numeric columns to numbers"""
        df = self._df
        for col in ES_Dataframe.to_numeric_list:
            df[col] = df[col].apply(pd.to_numeric, errors='coerce')
        self._df = df
        
    def apply_filters(self):
        df = self._df
        for filt in self._filters:
            if filt[1] == "=":
                df = df[df[filt[0]] == filt[2]]
            elif filt[1] == ">":
                df = df[df[filt[0]] > filt[2]]
            elif filt[1] == "<":
                df = df[df[filt[0]] < filt[2]]
        self._df = df
        import pdb; pdb.set_trace()
        app.logger.info("Filters applied")

if __name__ == '__main__':
    d = datetime.datetime(2016, 10, 25).strftime('%Y-%m-%d')
    # es = EquityStats(['test'], ['s'])
    es_df = ES_Dataframe(date=d)