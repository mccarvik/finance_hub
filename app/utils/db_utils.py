import pymysql.cursors
import pymysql
import sys
sys.path.append("/home/ubuntu/workspace/finance")
from app import app


from config import DBUSER, DBPASSWORD, DB, DBHOST

class DBHelper:
    '''Class to help with DB actions'''
    def __init__(self):
        self.cnx = None
        self.cursor = None
    
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
            self.cursor.execute(exec_string)
            for row in self.cursor:
                print(row)
        except Exception as e:
            app.logger.info("DB SELECT ERROR:" + str(e))

    
if __name__ == '__main__':
    a = DBHelper()
    a.connect(db_host='localhost')
    a.select('eq_screener')
    # db_connect()