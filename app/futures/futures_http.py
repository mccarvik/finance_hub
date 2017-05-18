from app import app

def post(request):
    # import pdb; pdb.set_trace()
    if request.form['action'] == 'fut_calc':
        fut_calc(request)

def fut_calc(request):
    print("Futures CALCULATOR")

    try:
        fut_for = request.form.get('fut_for', 'for')
        und = float(request.form.get('und', 100))
        r = float(request.form.get('ir', 0.00))
        t = float(request.form.get('tenor', 1))
        inc_yld = float(request.form.get('inc_yld', 0))
        conv_yld = float(request.form.get('conv_yld', 0))
        cst_cry = float(request.form.get('cst_cry', 0))
        import pdb; pdb.set_trace()
        price = request.form.get('price', None)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        app.logger.info("Error in option vanilla vars {0}, {1}, {2}".format(exc_type, exc_tb.tb_lineno, exc_obj))
        return
    
    forward = Futures(fut_for, und=und, ir=r, t=t, inc_yld=inc_yld, conv_yld=conv_yld, cst_cry=cst_cry, p=price)
    if not price:
        print(forward._price)
    else:
        print(forward._value)