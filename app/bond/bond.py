# Need this to get the paths for the imports straight
import sys
sys.path.append("/home/ubuntu/workspace/finance")

def post(request):
    # if request.form
    
    # import pdb; pdb.set_trace()
    if request.form['action'] == 'bond_calc':
        bond_calc(request)

def bond_calc(request):
    print("BOND CALCULATOR")