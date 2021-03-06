import json, pdb
from collections import OrderedDict
from flask import render_template, redirect, url_for, request, g, jsonify
from datetime import datetime
from app import app
from .forms import EditForm, PostForm, SearchForm
from .emails import follower_notification
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS, LANGUAGES, DATABASE_QUERY_TIMEOUT
from .equity.screener_eqs.equity_screener import post as eqsc_post
from .equity.analysis_eqs.equity_analysis_http import post as eqanal_post
from .futures.futures_http import post as fut_post
from .bond.tsy import post as tsy_post
from .options.vanilla.opt_vanilla import post as opt_vanilla_post

@app.route('/', methods=['GET', 'POST'])
def home(page=1):
    return render_template('home.html',
                           title='Home')

@app.route('/equity_screener', methods=['GET', 'POST'])
def equity_screener():
    column_map = {}
    with open("/home/ubuntu/workspace/finance/app/equity_screener/screen_info.csv", "r") as f:
        cols = str.split(f.readline(), ",")[1:]
        cols_desc = str.split(f.readline(), ",")[1:]
    ns_vals = sorted(zip(cols, cols_desc))
    
    if request.method == 'POST':
        ret = eqsc_post(request)
        if request.form['action'] == 'run_screening':
            # return json.dumps({'status':'OK','data': ret})
            return json.dumps(ret)
    
    return render_template('equity_screener.html',
                            title='Equity Screener',
                            num_screen_vals=ns_vals,
                            data=None)
                           

@app.route('/equity_analysis', methods=['GET', 'POST'])
def equity_analysis():
    # NOTE post method does not need to return a render
    if request.method == 'POST':
        post_ret = eqanal_post(request)
        return json.dumps(post_ret[1])
    elif request.method == 'GET':
        return render_template('equity_analysis.html',
                                title='Equity Analysis'), 200

@app.route('/tsy', methods=['GET', 'POST'])
def tsy():
    if request.method == 'POST':
        tsy_post(request)
    return render_template('tsy.html',
                           title='Treasuries')

@app.route('/bond', methods=['GET', 'POST'])
def bond():
    if request.method == 'POST':
        bond_post(request)
    return render_template('bond.html',
                           title='Bond Calculator')

@app.route('/futures_calc', methods=['GET', 'POST'])
def futures_calc():
    if request.method == 'POST':
        fut_post(request)
    return render_template('futures_calc.html',
                           title='Futures Calculator')

@app.route('/opt_analysis', methods=['GET', 'POST'])
def opt_analysis():
    # if request.method == 'POST' or request.method=='GET':
    if request.method == 'POST':
        eqanal_post(request)
    return render_template('opt_analysis.html',
                           title='Option Analysis'), 200

@app.route('/option/vanilla', methods=['GET', 'POST'])
def opt_vanilla():
    if request.method == 'POST':
        opt_vanilla_post(request)
    return render_template('opt_vanilla.html',
                           title='Options - Vanilla')
                           
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500




