def post(request):
    # import pdb; pdb.set_trace()
    if request.form['action'] == 'run_screening':
        run_screening(request)

def run_screening(request):
    print("RUN SCREENING")