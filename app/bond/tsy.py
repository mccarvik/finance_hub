# Need this to get the paths for the imports straight
import sys
sys.path.append("/home/ubuntu/workspace/finance")

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
    print("got here")


