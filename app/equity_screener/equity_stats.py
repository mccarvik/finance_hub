import datetime
import urllib.request
import re

column_opts = []

class EquityStats():
    """holds all the individual stats for a stock
    like P/E, dividend yield, etc.
    """
    
    def __init__(self, ticker):
        self._ticker = ticker
        self.key_stats = self.keyStatFunc()
    
    def getHtmlText(self):
        symbol = self._ticker
        url = 'https://www.google.com/finance?q=NASDAQ%3A' + symbol + '&ei=kdenV4HtL5WmeavUg5AL'
        htmlFile = urllib.request.urlopen(url)
        html_text = htmlFile.read()
        return html_text
    
    @staticmethod
    def setColumns():
        #could pick any, just setting a standard set of columns
        symbol = "FLWS"
        url = 'https://www.google.com/finance?q=NASDAQ%3A' + symbol + '&ei=kdenV4HtL5WmeavUg5AL'
        htmlFile = urllib.request.urlopen(url)
        html_text = htmlFile.read()
        fields_re = 'data-snapfield(.+?)>(.+?)</td>(.+?)<td class="val">(.+?)</td>'
        data = re.findall(re.compile(fields_re), str(html_text))
        cols = []
        for i in data:
            cols.append(str(i[1]).replace("\\n",""))
        cols = EquityStats._cleanCols(cols)
        EquityStats.cols = cols
    
    def _cleanCols(cols):
        final_cols = ["Symbol"]
        for c in cols:
            if c in ("Range", "52 week"):
                final_cols.append(c + " hi")
                final_cols.append(c + " lo")
            elif c == "Vol / Avg.":
                c = c.replace(" ","").split("/")
                final_cols.append(c[0])
                final_cols.append(c[1])
            elif c == "Div/yield":
                c = c.replace(" ","").split("/")
                final_cols.append(c[0])
                final_cols.append("Div " + c[1])
            else:
                final_cols.append(c)
        return final_cols
                
    
    #enter a stock symbol
    def keyStatFunc(self):
        html_text = self.getHtmlText()
        fields_re = 'data-snapfield(.+?)>(.+?)</td>(.+?)<td class="val">(.+?)</td>'
        data = re.findall(re.compile(fields_re), str(html_text))
        vals = []
        for i in data:
            if "&nbsp" not in i[3]:#
                vals.append(str(i[3]).replace("\\n",""))
            else:
                vals.append("")
        vals = [self._ticker] + self._cleanStats(vals)
        return vals
    
    def _cleanStats(self, vals):
        final_vals = []
        #Bunch of one off scenarios that are annoying but need to be dealt with
        ct=0
        for v in vals:
            #range and 52 week
            if ct == 0 or ct == 1:
                if v:
                    v = v.replace(" ", "").split("-")
                    final_vals.append(self._cleanIndVal(v[0]))
                    final_vals.append(self._cleanIndVal(v[1]))
                else:
                    final_vals.append(None)
                    final_vals.append(None)
            elif ct == 3:
                if v:
                    v = v.replace(" ", "").split("/")
                    final_vals.append(self._cleanIndVal(v[0]))
                    final_vals.append(self._cleanIndVal(v[1]))
                else:
                    final_vals.append(None)
                    final_vals.append(None)
            elif ct == 6:
                if v:
                    v = v.replace(" ", "").split("/")
                    final_vals.append(self._cleanIndVal(v[0]))
                    final_vals.append(self._cleanIndVal(v[1]))
                else:
                    final_vals.append(None)
                    final_vals.append(None)
            else:
                if v:
                    final_vals.append(self._cleanIndVal(v))
                else:
                    final_vals.append(None)
            ct+=1
        return final_vals
        
    def _cleanIndVal(self, val):
        val = val.replace(",","")
        # Need to do something smarter here at some point
        if val[-1] in ("%", "B", "M"):
            val = val[:-1]
        if val.isdigit():
            return(float(val))
        else:
            return(val)