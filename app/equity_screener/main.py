import create_symbols
from equity_stats import EquityStats
import pandas as pd


def main(sim=False):
    # Go thru the Zile, read each ticker and try to collect data
    reader = open("memb_list.txt", "r")
    eqs = []
    EquityStats.setColumns()
    with open("memb_list.txt", "r") as f:
        ct = 0
        for line in f:
            eqs.append(EquityStats(line.strip()))
            print("finished {0}".format(line.strip()))
            #TEMP
            ct += 1
            if ct==10: break
            
    
    #build dataframe
    arr_2d = []
    for e in eqs:
        lyst = e.key_stats
        arr_2d.append(lyst)
    df = pd.DataFrame(data=arr_2d, columns=EquityStats.cols)
    filters = getFilters(sim)

    print(df.to_string())
    for f in filters:
        print(f)
        try:
            df[f[0]] = df[f[0]].astype(float)
        except Exception as e:
            print(e, " filter not applied")
            continue
        if f[1] == "=":
            df = df[df[f[0]] == f[2]]
        elif f[1] == ">":
            df = df[df[f[0]] > f[2]]
        elif f[1] == "<":
            df = df[df[f[0]] < f[2]]
        print(df.to_string())

def getFilters(sim):
    filters = []
    
    if not sim:
        while True:
            print("Select satistic:")
            [print(i + ",  ", end="") for i in EquityStats.cols]
            stat = input()
            if not stat:
                break
            print('Select conditon:')
            print('< or >')
            condition = input()
            print('Select value:')
            val = input()
            filters.append((stat, condition, val))
    else:
        filters.append(("P/E", "<", 20))
        filters.append(("Beta", "<", 2))
        filters.append(('Div yield', '>', 1))
    return filters


#create_symbols.create_symbols()

main(sim=True)