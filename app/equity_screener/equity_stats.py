import datetime
import re
import os
from app.utils.db_utils import DBHelper

column_opts = []

class EquityStats():
    """holds all the individual stats for a stock
    like P/E, dividend yield, etc.
    """
    
    def __init__(self, stats, col_list, write=True):
        self._stats = dict(zip(col_list, stats))
        self._ticker = self._stats['s']
        if write:
            self.write_to_db()
    
    def write_to_db(self):
        db = DBHelper()
        db.connect()
        pass
    
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