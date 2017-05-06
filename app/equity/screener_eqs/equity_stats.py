import sys
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import datetime
import re, os, string, json, types, pdb
import pandas as pd
import numpy as np
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
        
        if self._source == "API1":
            self._stats = dict(zip(col_list, stats))
            self._ticker = self._stats['s']
            self._stats['date'] = self._date
        elif self._source == "API2":
            self._stats = stats
            self._ticker = self._stats['ticker']
            self._stats['date'] = self._date
        
        if write:
            self.write_to_db()
    
    def write_to_db(self):
        with DBHelper() as db:
            db.connect()
            if self._source == "API1":
                table = 'eq_screener'
                self._stats['n'] = self._stats['n'].replace("'", "''")
                prim_keys = ['date', 's']
            elif self._source == "API2":
                table = 'eq_screener2'
                self._stats['ticker'] = self._stats['ticker'].replace("'", "''")
                prim_keys = ['date', 'ticker']
            db.upsert(table, self._stats, prim_keys)
    
    @staticmethod
    def setColumns(source):
        # TODO set the columns and set the favorites here from the file, lets get them out of the code
        column_map = {}
        if source == "API1":
            file = "/home/ubuntu/workspace/finance/app/equity/screener_eqs/yahoo_api1_notes.txt"
        elif source == "API2":
            file = "/home/ubuntu/workspace/finance/app/equity/screener_eqs/yahoo_api2_notes.txt"
        with open(file, "r") as f:
            for line in f:
                if line.strip() == 'EOF':
                    break
                t_tup = line.split(' ')
                column_map[t_tup[0]] = " ".join(t_tup[1:]).strip()
        EquityStats.cols = column_map
            


class ES_Dataframe:
    """HOlds the dataframe of a call to the eq_screener DB
    and preforms all the filters"""
    
    test_filters = [('r', '<', 15),  ('y', '>', 2), ('m6', '<', 0), ('m8', '<', 0), ('r5', '<', 1)]
    
    def __init__(self, date=None, filters=None, favs=False):
        self._favs = favs
        self._filters = filters or ES_Dataframe.test_filters
        self._colmap = self.setColumns()
        self._date = date or datetime.datetime.now().strftime('%Y-%m-%d')
        pdb.set_trace()
        self._df = self.read_from_db(table='eq_screener2')
        self.readOther()
        self.clean_data()
        self.apply_filters()
        self.cleanForPresentation()
        
    def cleanForPresentation(self):
        df = self._df
        # Removing NaNs so it can be put in a JSON
        df = df.replace(np.nan,' ', regex=True)
        # order columns
        df = df.reindex_axis(sorted(df.columns), axis=1)
        
        self._df = df
        
    def readOther(self):
        file = "/home/ubuntu/workspace/finance/app/equity_screener/yahoo_api2_notes.txt"
        other = False
        with open(file, "r") as f:
            for line in f:
                if other:
                    nn = line.strip()
                    date_to_string = f.readline().strip()
                    break
                if line.strip() == 'Other':
                    other = True
        self._nonnumeric = nn.split(",")
        self._date_to_string = date_to_string.split(",")
    
    def read_from_db(self, table):
        with DBHelper() as db:
            db.connect()
            return db.select(table, where="date='{0}'".format(self._date))
        
    @staticmethod
    def setColumns():
        column_map = {}
        with open("/home/ubuntu/workspace/finance/app/equity/screener_eqs/screen_info.csv", "r") as f:
            cols = str.split(f.readline(), ",")[1:]
            cols_desc = str.split(f.readline(), ",")[1:]
        return dict(zip(cols, cols_desc))    
    
    def clean_data(self):
        """moves around data in the dataframe for screening purposes"""
        # self.removePunctuation()
        self.numberfy()
        app.logger.info("Done cleaning data")
    
    def removePunctuation(self):
        """replacing punctiation in all the columns"""
        # Doesnt really work, lot of errors on None values
        # Also might not be necessary
        df = self._df
        for col in df.columns:
            if not isinstance(df[col][0], str):
                continue
            for pct in ['+', '%']:
                try:
                    df[col] = df[col].apply(lambda x: x.replace(pct,""))
                except Exception as e:
                    print("column prob doesnt need punctiation cleaning" + e)
                    break
                    # exc_type, exc_obj, exc_tb = sys.exc_info()
                    # app.logger.info("PANDAS DATA CLEAN ERROR: {0}, {1}, {2}".format(exc_type, exc_tb.tb_lineno, exc_obj))
        self._df = df
    
    def numberfy(self):
        """sets all the numeric columns to numbers"""
        df = self._df
        for col in df.columns:
            if col not in self._nonnumeric:
                df[col] = df[col].apply(pd.to_numeric, errors='coerce')
            if col in self._date_to_string:
                # Need this to convert certain datetimes to strings
                df[col] = df[col].apply(lambda x: x.strftime("%Y%m%d"))
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