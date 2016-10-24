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
            # app.logger.info('Successfully connected to ' + database)
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
            exc_type, exc_obj, exc_tb = sys.exc_info()
            app.logger.info("DB SELECT ERROR: {0}, {1}, {2}".format(exc_type, exc_tb.tb_lineno, exc_obj))
            return {'status': 500}
    
    def update(self, table, cols, vals, where):
        exec_string = 'UPDATE {0}'.format(table)
        set_string = ' SET '
        vals =stringify(vals)
        for c,v in zip(cols, vals):
            set_string += '{0}={1}, '.format(c,v)
        set_string = set_string[:-2]
        exec_string += set_string
        exec_string += " WHERE {0}".format(where)
        
        try:
            self.cursor.execute(exec_string)
            self.cnx.commit()
            return {'status': 200}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            import pdb; pdb.set_trace()
            app.logger.info("DB UPDATE ERROR: {0}, {1}, {2}".format(exc_type, exc_tb.tb_lineno, exc_obj))
            return {'status': 500}
    
    def insert_into(self, table, cols, vals):
        vals = stringify(vals)
        exec_string = 'INSERT INTO {0} '.format(table)
        col_string = "(" + ",".join(cols) + ")"
        val_string = "VALUES (" + ",".join(vals) + ")"
        exec_string += """
                        {0}
                        {1}""".format(col_string, val_string)
        try:
            self.cursor.execute(exec_string)
            self.cnx.commit()
            return {'status': 200}
        except pymysql.err.IntegrityError as e:
            # Duplicate entry for this insert
            return {'status': 500}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            import pdb; pdb.set_trace()
            app.logger.info("DB INSERT INTO ERROR: {0}, {1}, {2}".format(exc_type, exc_tb.tb_lineno, exc_obj))
            return {'status': 500}
            
    
    def upsert(self, table, cols_vals, prim_keys):
        # first try an insert
        try:
            ret = self.insert_into(table, cols_vals.keys(), list(cols_vals.values()))
            if ret['status'] == 200:
                self.cnx.commit()
            else:
                raise Exception('Error in insert statement (Probably a duplicate')
        except:
            try:
                # if error try update (need to build where clause first)
                w_c = ""
                for pk in prim_keys:
                    w_c += pk + "=" + stringify(cols_vals[pk]) + " AND "
                w_c = w_c[:-5]
                self.update(table, cols_vals.keys(), list(cols_vals.values()), w_c)
                self.cnx.commit()
                return {'status': 200}
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                app.logger.info("DB UPSERT ERROR: {0}, {1}, {2}".format(exc_type, exc_tb.tb_lineno, exc_obj))
                return {'status': 500}
                
            
            
if __name__ == '__main__':
    a = DBHelper()
    a.connect(db_host='localhost')
    a.upsert('eq_screener', {'date':'2015-10-20', 's':'test2', 'n':'test22'}, ['date', 's'])