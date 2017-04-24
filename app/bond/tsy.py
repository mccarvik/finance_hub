# Need this to get the paths for the imports straight
import sys
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import pdb, requests, datetime
from app import app
import pandas as pd

def post(request):
    ''' Post method to receive all requests and send them to the appropriate method
    
    Parameters
    ==========
    request : Object
        specific request plusn ecessary variable for what user wants
    
    Return
    ======
    Object
        varies based on type of request
    '''
    
    # import pdb; pdb.set_trace()
    if request.form['action'] == 'get_data':
        get_data()

def get_data():
    ''' retrieves raw data for treasuries through api 
    
    Parameters
    ==========
    NONE
    
    Return
    ======
    Pandas Array
        raw data for the treasuries
    '''
    
    # returns all securities with maturity date > today
    url = 'https://www.treasurydirect.gov/TA_WS/securities/search?maturityDate >=today&format=json'
    test_url = 'https://www.treasurydirect.gov/TA_WS/securities/TIPS?format=json'
    try:
        req = requests.get(url)
    except Exception as e:
        pdb.set_trace()
        exc_type, exc_obj, exc_tb = sys.exc_info()
        app.logger.info("API GRAB ERROR: {0}, {1}, {2}".format(exc_type, exc_tb.tb_lineno, exc_obj))
    
    tsy_df = pd.read_json(req.content.decode('utf-8'))
    import pdb; pdb.set_trace()
    print("got here")


# Used for testing
if __name__ == '__main__':
    get_data()