import pymysql.cursors
import pymysql
import datetime
import sys
sys.path.append("/home/ubuntu/workspace/finance")
from app import app
from app.utils.helper_funcs import stringify


from config import DBUSER, DBPASSWORD, DB, DBHOST

class DBHelper:
    '''Class to help with DB actions'''
    def __init__(self):
        self.cnx = None
        self.cursor = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.cnx:
            self.cnx.close()
    
    def connect(self, database=DB, db_user=DBUSER, db_password=DBPASSWORD, db_host=DBHOST):
        try:
            self.cnx = pymysql.connect(user=db_user, password=db_password,
                                  host=db_host,database=database)
            self.cursor = self.cnx.cursor()
            # import pdb; pdb.set_trace()
            app.logger.info('Successfully connected to ' + database)
        except Exception as e:
            app.logger.info('COULD NOT CONNECT TO ' + database)
            app.logger.info("DB ERROR:" + str(e))
    
    def select(self, table, cols =['*'], where=None):
        cols = ",".join(cols)
        exec_string = '''SELECT {0} 
                         FROM {1} '''.format(cols,table)
        if where:
            exec_string += "WHERE {0}".format(where)
        try:
            import pdb; pdb.set_trace()
            self.cursor.execute(exec_string)
            for row in self.cursor:
                print(row)
        except Exception as e:
            app.logger.info("DB SELECT ERROR:" + str(e))
    
    def update(self, table, cols, vals, where=None):
        exec_string = 'UPDATE {0}'.format(table)
        set_string = 'SET '
        for c,v in cols, vals:
            set_string += '{0}={1}, '.format(c,v)
        set_string = set_string[:-1]
        if where:
            exec_string += "WHERE {0}".format(where)
        
        try:
            import pdb; pdb.set_trace()
            self.cursor.execute(exec_string)
            for row in self.cursor:
                print(row)
        except Exception as e:
            app.logger.info("DB UPDATE ERROR:" + str(e))
    
    def insert_into(self, table, cols, vals):
        vals = stringify(vals)
        exec_string = 'INSERT INTO {0} '.format(table)
        col_string = "(" + ",".join(cols) + ")"
        val_string = "VALUES (" + ",".join(vals) + ")"
        exec_string += """
                        {0}
                        {1}""".format(col_string, val_string)
        try:
            import pdb; pdb.set_trace()
            self.cursor.execute(exec_string)
            self.cnx.commit()
        except Exception as e:
            app.logger.info("DB UPDATE ERROR:" + str(e))
    
    def upsert(self, table, cols, vals, where=None):
        pass
    
if __name__ == '__main__':
    a = DBHelper()
    a.connect(db_host='localhost')
    a.insert_into('eq_screener', ['date', 's'], ['2016-10-20','test'])