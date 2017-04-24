# Need this to get the paths for the imports straight
import sys
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import pdb, requests, datetime, time
import pandas as pd
from app import app.bond
from .bond import Bond
from .bond.FixedRateBond import FixedRateBond


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
    # TODO: front of this if statement used for testing
    if not request or request.form['action'] == 'get_data':
        tsy_df = get_api_data()
        tsy_df = filter_array(tsy_df)
        tsy_df = setup_bonds(tsy_df)

def get_api_data():
    ''' retrieves raw data for treasuries through api 
    
    Parameters
    ==========
    NONE
    
    Return
    ======
    Pandas Array
        all raw data for the treasuries that are not matured
    '''
    
    # returns all securities with maturity date > today
    # TODO: maturity date filter for non matured bonds not working, returns all bonds
    t0 = time.time()
    url = 'https://www.treasurydirect.gov/TA_WS/securities/search?maturityDate >=today&format=json'
    test_url = 'http://www.treasurydirect.gov/TA_WS/securities/Bond?format=json'
    try:
        req = requests.get(test_url)
    except Exception as e:
        pdb.set_trace()
        exc_type, exc_obj, exc_tb = sys.exc_info()
        app.logger.info("API GRAB ERROR: {0}, {1}, {2}".format(exc_type, exc_tb.tb_lineno, exc_obj))
    
    tsy_df = pd.read_json(req.content.decode('utf-8'))
    tsy_df = tsy_df[tsy_df['maturityDate'] > str(datetime.date.today())]
    t1 = time.time()
    print("took {0} seconds to grab data from API".format(t1-t0))
    return tsy_df
    
def filter_array(tsy_df):
    ''' removes unnecessary columns and does any other desired filtering
    
    Parameters
    ==========
    tsy_df = pandas df
        array of raw data from api
        
    Return
    ======
    tsy_df = pandas df
        filtered array
    '''
    tsy_df = tsy_df[['cusip','issueDate','maturityDate','securityType','interestRate','callable',
                    'firstInterestPaymentDate','averageMedianPrice','averageMedianYield']]
    return tsy_df

def setup_bonds(tsy_df):
    ''' Take the filtered array and setup bond based on type
    
    Parameters
    ==========
    tsy_df = pandas df
        array of filtered bond data
    
    Return
    ======
    tsy_df = pandas df
        array of bond objects, no longer just raw data
    '''
    import pdb; pdb.set_trace()
    new_df = tsy_df.apply(lambda t: FixedRateBond(t.cusip, t.issueDate, t.maturityDate, t.securityType))
    for t in tsy_df.values:
        import pdb; pdb.set_trace()
        new_df.append(FixedBond())

# Used for testing
if __name__ == '__main__':
    post(None)