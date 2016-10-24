import sys
sys.path.append("/home/ubuntu/workspace/finance")
import datetime
import re
import os
import pandas as pd
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
        with open("/home/ubuntu/workspace/finance/app/static/docs/yahoo_api_notes.txt", "r") as f:
            for line in f:
                if line.strip() == 'EOF':
                    break
                t_tup = line.split('\t')
                column_map[t_tup[0]] = t_tup[1]
        EquityStats.cols = column_map


class ES_Dataframe:
    """HOlds the dataframe of a call to the eq_screener DB
    and preforms all the filters"""
    
    def __init__(self, date=None, filters=None):
        self._filters = filters
        self._colmap = self.setColumns()
        self._date = date or datetime.datetime.now().strftime('%Y-%m-%d')
        self._df = self.read_from_db()
        import pdb; pdb.set_trace();
        pass
    
    def read_from_db(self):
        with DBHelper() as db:
            db.connect()
            return db.select('eq_screener', where="date='{0}'".format(self._date))
        
        
    @staticmethod
    def setColumns():
        column_map = {}
        with open("/home/ubuntu/workspace/finance/app/static/docs/yahoo_api_notes.txt", "r") as f:
            for line in f:
                if line.strip() == 'EOF':
                    break
                t_tup = line.split('\t')
                column_map[t_tup[0]] = t_tup[1]
        return column_map
    


if __name__ == '__main__':
    es = EquityStats(['test'], ['s'])