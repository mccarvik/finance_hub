import sys
sys.path.append("/home/ubuntu/workspace/finance")
import datetime
import re, os, string, json, types
import pandas as pd
import requests
from app import app
from app.utils.db_utils import DBHelper
from bs4 import BeautifulSoup

column_opts = []

class EquityStats():
    """holds all the individual stats for a stock
    like P/E, dividend yield, etc.
    """
    
    def __init__(self, stats, col_list, source, write=False, date=None):
        self._date = date or datetime.datetime.now().strftime('%Y-%m-%d')
        self._source = source
        
        if self._source == "API"
            self._stats = dict(zip(col_list, stats))
            self._ticker = self._stats['s']
            self._stats['date'] = self._date
        elif self._source == "SCRAPE":
            
        # self.add_scraped_columns()
        
        if write:
            self.write_to_db()
    
    def write_to_db(self):
        with DBHelper() as db:
            db.connect()
            self._stats['n'] = self._stats['n'].replace("'", "''")
            db.upsert('eq_screener', self._stats, ['date', 's'])
    
    def add_scraped_columns(self):
        with open("/home/ubuntu/workspace/finance/app/equity_screener/yahoo_scrape_notes.txt", "r") as f:
            url = f.readline().replace('$$$$', self._ticker)
        data = requests.get(url).json()['quoteSummary']['result'][0]
        import pdb; pdb.set_trace()
        scraped_data = {}
        for main_key in data.keys():
            scraped_data = self.scraped_col_helper_recursive(scraped_data, data, main_key)
            import pdb; pdb.set_trace()
        sys.exit()
    
        
    def scraped_col_helper_recursive(self, scraped_data, data, key):
        import pdb; pdb.set_trace()
        try:
            scraped_data[key] = data[key]['raw']
        except:
            try:
                t_data = data[key]
                if isinstance(t_data, dict) and t_data:
                    for key2 in t_data.keys():
                        scraped_data = self.scraped_col_helper_recursive(scraped_data, t_data, key2)
                elif isinstance(t_data, list) and t_data:
                    # might need to adjust this
                    import pdb; pdb.set_trace()
                    scraped_data[key] = t_data[0]['raw']
                elif t_data:
                    scraped_data[key] = t_data
                else:
                    print("data is fucked or empty, setting the val to an empty string {0}".format(key))
                    scraped_data[key] = ""
            except:
                print("SUM TING WONG")
        return scraped_data

    
    @staticmethod
    def setColumns(source):
        # TODO set the columns and set the favorites here from the file, lets get them out of the code
        column_map = {}
        if source == "API"
            with open("/home/ubuntu/workspace/finance/app/equity_screener/yahoo_api_notes.txt", "r") as f:
                for line in f:
                    if line.strip() == 'EOF':
                        break
                    t_tup = line.split('\t')
                    column_map[t_tup[0]] = t_tup[1]
            EquityStats.cols = column_map
        elif source == "SCRAPE":
            pass


class ES_Dataframe:
    """HOlds the dataframe of a call to the eq_screener DB
    and preforms all the filters"""
    
    exempt_list = ['l', 'i', 's', 'n', 'w', 'e1', 'm', 'm2', 'n4', 'x']
    to_numeric_list = ['a', 'a2', 'a5', 'b', 'b2', 'b3', 'b4', 'b6', 'c', 'c1', 'c3', 'c6', 'c8', 'd', 'e',
                        'e7', 'e8', 'e9', 'f6', 'g', 'h', 'j', 'k', 'g1', 'g3', 'g4', 'g5', 'g6', 'j1', 'j3', 
                        'j4', 'j5', 'j6', 'k1', 'k2', 'k3', 'k4', 'k5', 'l1', 'l2', 'l3', 'm3', 'm4', 'm5',
                        'm6', 'm7', 'm8', 'o', 'p', 'p1', 'p2', 'p5', 'p6', 'r', 'r2', 'r5', 'r6', 'r7', 's1',
                        's7', 't6', 't7', 't8', 'v', 'v1', 'v7', 'w1', 'w4', 'y']
    fav_list = ['a', 'a2', 'a5', 'b', 'b4', 'b6', 'd', 'e', 'e7', 'e8', 'e9', 'f6', 'j', 'k', 'j1', 'j4',
                'j5', 'j6', 'k4', 'k5', 'l1', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'p', 'p5', 'p6', 'r', 'r5',
                'r6', 'r7', 's7', 't8', 'v', 'w1', 'y']
                
    test_filters = [('r', '<', 15),  ('y', '>', 2), ('m6', '<', 0), ('m8', '<', 0), ('r5', '<', 1)]
    
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
        cols_desc = [self._colmap[k].strip() for k in cols]
        cols_favs_desc = [self._colmap[k].strip() for k in ES_Dataframe.fav_list]
        with open('/home/ubuntu/workspace/finance/app/equity_screener/screen_info.csv', 'w') as f:
            f.write("columns," + ",".join(cols) + '\n')
            f.write("columns description," + ",".join(cols_desc) + '\n')
            f.write("favorites," + ",".join(ES_Dataframe.fav_list) + '\n')
            f.write("favorites description," + ",".join(cols_favs_desc) + '\n')
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
            try:
                if filt[1] == "=":
                    df = df[df[filt[0]] == filt[2]]
                elif filt[1] == ">":
                    df = df[df[filt[0]] > filt[2]]
                elif filt[1] == "<":
                    df = df[df[filt[0]] < filt[2]]
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                app.logger.info("COULD NOT APPLY FILTER: {0}, {1}, {2}".format(exc_type, exc_tb.tb_lineno, exc_obj))
        self._df = df
        app.logger.info("Filters applied")

if __name__ == '__main__':
    # import pdb; pdb.set_trace()
    d = datetime.datetime(2016, 10, 25).strftime('%Y-%m-%d')
    es_df = ES_Dataframe(date=d)