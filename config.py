# -*- coding: utf8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

WHOOSH_BASE = os.path.join(basedir, 'search.db')

# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5

# email server
MAIL_SERVER = 'your.mailserver.com'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# available languages
LANGUAGES = {
    'en': 'English',
    'es': 'Español'
}

# microsoft translation service
MS_TRANSLATOR_CLIENT_ID = '' # enter your MS translator app id here
MS_TRANSLATOR_CLIENT_SECRET = '' # enter your MS translator app secret here

# administrator list
ADMINS = ['you@example.com']

# pagination
POSTS_PER_PAGE = 50
MAX_SEARCH_RESULTS = 50


DBUSER = 'root'
DBPASSWORD = ''
DB = 'finance'
# DBHOST = 'mccarvik-playground-2305615'
# DBPASSWORD = 'kmac7272'
DBHOST = 'localhost'

FRED_API_KEY = '37c0d190aa9135031d213194f0930142'
IMG_PATH = "/home/ubuntu/workspace/finance/app/static/img/"

QUANDL_API_KEY = 'J4d6zKiPjebay-zW7T8X'