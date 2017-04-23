# Need this to get the paths for the imports straight
import sys
sys.path.append("/home/ubuntu/workspace/finance")

def post(request):
    # import pdb; pdb.set_trace()
    if request.form['action'] == 'get_data':
        get_data()

def get_data():
    print("got here")

def bond_calc(request):
    print("BOND CALCULATOR")