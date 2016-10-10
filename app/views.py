from flask import render_template, flash, redirect, session, url_for, request, \
    g, jsonify
from flask_login import login_user, logout_user, current_user, \
    login_required
from flask_sqlalchemy import get_debug_queries
from flask_babel import gettext
from datetime import datetime
from guess_language import guessLanguage
from app import app, db, lm, oid, babel
from .forms import LoginForm, EditForm, PostForm, SearchForm
from .models import User, Post
from .emails import follower_notification
from .translate import microsoft_translate
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS, LANGUAGES, \
    DATABASE_QUERY_TIMEOUT

from .equity_screener.equity_screener import post as eqsc_post
from .bond.bond import post as bond_post


@app.route('/', methods=['GET', 'POST'])
def home(page=1):
    return render_template('home.html',
                           title='Home')

@app.route('/equity_screener', methods=['GET', 'POST'])
def equity_screener():
    num_screen_vals = ['PE', 'Div Yield']
    if request.method == 'POST':
        eqsc_post(request)
    return render_template('equity_screener.html',
                           title='Equity Screener',
                           num_screen_vals=num_screen_vals)
                           
@app.route('/bond', methods=['GET', 'POST'])
def bond():
    if request.method == 'POST':
        bond_post(request)
    return render_template('bond.html',
                           title='Bond Calculator')

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = get_locale()


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500




