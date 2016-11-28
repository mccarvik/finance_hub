from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask_babel import gettext
from datetime import datetime
from guess_language import guessLanguage
from app import app
from .forms import EditForm, PostForm, SearchForm
from .emails import follower_notification
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS, LANGUAGES, \
    DATABASE_QUERY_TIMEOUT
from .equity_screener.equity_screener import post as eqsc_post
from .bond.bond import post as bond_post
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
    ns_vals = dict(zip(cols, cols_desc))
    
    if request.method == 'POST':
        ret = eqsc_post(request)
        if request.form['action'] == 'run_screening':
            import pdb; pdb.set_trace()
            return render_template('equity_screener.html',
                                    title='Equity Screener',
                                    num_screen_vals=ns_vals,
                                    data=ret)
                                    
    return render_template('equity_screener.html',
                            title='Equity Screener',
                            num_screen_vals=ns_vals,
                            data=None)
                           
@app.route('/bond', methods=['GET', 'POST'])
def bond():
    if request.method == 'POST':
        bond_post(request)
    return render_template('bond.html',
                           title='Bond Calculator')

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




