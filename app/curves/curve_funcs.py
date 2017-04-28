from bs4 import BeautifulSoup as bs
import requests, re

def loadTreasuryCurve():
    ''' uses beautiful soup to scrape treasury xml for curve points'''
    
    url = 'http://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=month(NEW_DATE)%20eq%204%20and%20year(NEW_DATE)%20eq%202017'
    