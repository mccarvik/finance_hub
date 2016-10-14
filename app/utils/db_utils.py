import pymysql.cursors
import pymysql
import sys
sys.path.append("/home/ubuntu/workspace/finance")
from app import app


from config import DBUSER, DBPASSWORD, DB, DBHOST

def db_connect(database=DB,db_user=DBUSER,db_password=DBPASSWORD,db_host=DBHOST):
    try:
        cnx = pymysql.connect(user=db_user, password=db_password,
                              host=db_host,database=database)
        # import pdb; pdb.set_trace()
        app.logger.debug('Successfully connected to ' + database)
    except Exception as e:
        print("DB ERROR:" + str(e))
    
if __name__ == '__main__':
    db_connect(db_host='localhost')
    # db_connect()