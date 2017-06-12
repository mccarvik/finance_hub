# FORMAT: name : [database_code, dataseries_code]
from config import QUANDL_API_KEY

URL = 'https://www.quandl.com/api/v3/datasets/{0}/{1}/data.csv?start_date={2}&end_date={3}&api_key=' + QUANDL_API_KEY
quandl_api_dict = {
    'corn' : ['CME', 'C'],
    'gold' : ['CME', 'GC'],
}

MONTH_MAP = {
    1 : 'F',
    2 : 'G',
    3 : 'H',
    4 : 'J',
    5 : 'K',
    6 : 'M',
    7 : 'N',
    8 : 'Q',
    9 : 'U',
    10 : 'V',
    11 : 'X',
    12 : 'Z'
}