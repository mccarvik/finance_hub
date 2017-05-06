import time
import csv
import urllib.request
import sys
import os
import logging
import unicodedata

memb_list = "http://www.ftserussell.com/files/support-documents/membership-russell-3000"

logger = logging.getLogger('MyLogger')
logger.setLevel(logging.DEBUG)
db = logging.StreamHandler()
logger.addHandler(db)

def download_file(download_url):
    response = urllib.request.urlopen(download_url)
    file = open("memb_list.pdf", 'wb')
    logger.debug("File Downloaded")
    file.write(response.read())
    logger.debug("File Written")
    file.close()
    logger.debug("File Closed")
    
def write_tickers_to_file():
    tickers = []
    try:
        f = open('./memb_list_pdf.txt', 'rb')
        readFile = f.read().decode('utf8', 'ignore')
        splitFile = readFile.split('\n')
        for eachLine in splitFile:
            eachLine = eachLine.strip()
            splitLine = eachLine.split(' ')
            ticker = splitLine[-1]
            if ticker and len(ticker) < 5 and ticker.isupper():
                tickers.append(ticker)
    except Exception as e:
        logger.error("Issue on the file read %s" % e)
    
    try:
        writeFile = open('memb_list.txt','w')
        for t in tickers:
            writeFile.write(t+"\n")
        logger.debug("Ticker File Written")
        writeFile.close()
    except Exception as e:
        logger.error("Issue on the file write")

def convert_file():
    input="memb_list.pdf"
    output="memb_list_pdf.txt"
    os.system(("ps2ascii %s %s") %( input , output))
    logger.debug("File Converted")

def create_symbols():
    #download_file(memb_list)
    #convert_file()
    write_tickers_to_file()