def post(request):
    # import pdb; pdb.set_trace()
    if request.form['action'] == 'bond_calc':
        bond_calc(request)

def bond_calc(request):
    print("BOND CALCULATOR")