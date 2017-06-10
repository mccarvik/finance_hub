import sys
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import pdb, requests, datetime, csv
import pandas as pd
from config import QUANDL_API_KEY

URL = ['https://www.quandl.com/api/v3/datasets/', '/data.csv?api_key=' + QUANDL_API_KEY]

def callQuandlAPI(db_code, ds_code):
    url = "".join([URL[0], db_code + "/" + ds_code, URL[1]])
    urlData = requests.get(url).content.decode('utf-8')
    cr = csv.reader(urlData.splitlines(), delimiter=',')
    data = []
    for row in list(cr):
        data.append(row)
    df = pd.DataFrame(data)
    pdb.set_trace()
    print("")
    
if __name__ == '__main__':
    callQuandlAPI('WIKI', 'FB')