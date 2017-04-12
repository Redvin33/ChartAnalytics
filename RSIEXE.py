from datetime import *
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader as web


def RSI(data):
    AVG_gain = 0
    AVG_loss = 0

    for info in data.values:
        open = float(info[0])
        close = float(info[3])
        gainloss = close-open
        if gainloss > 0:
            AVG_gain += gainloss
        elif gainloss < 0:
            AVG_loss -= gainloss


    RS = AVG_gain/AVG_loss
    RSI = 100 - (100/(1+RS))

    return RSI


def main():
    symbol = input("Write symbol of the stock: ")
    timeframe = int(input("Choose dayrange: "))
    end = datetime.today()
    start = datetime.today()
    RSIlist = []
    dates = []
    i = 0

    while i < timeframe:
        start -= timedelta(days=1)
        if start.weekday() > 4:
            continue

        else:
            dates.append(start)
            i += 1



    for i in range(0, timeframe):
        df = web.DataReader(symbol, "yahoo", start-timedelta(days=i), end - timedelta(days=i))
        RSIlist.append(RSI(df))
    plt.plot(dates, RSIlist)
    plt.show()

main()
