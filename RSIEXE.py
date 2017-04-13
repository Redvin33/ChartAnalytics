from datetime import *
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader as web

#counts RSI for specific timeframe and date more info from RSI
#link: http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:relative_strength_index_rsi
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

#Eliminates weekends because theyre not business days
def weekendEliminator(end, timeframe):
    i = 0
    while i < timeframe:
        end -= timedelta(days=1)
        print(end)
        if end.weekday() > 4:
            continue

        else:
            i += 1
    return end



def main():
    symbol = input("Write symbol of the stock: ")
    timeframe = int(input("Choose dayrange: "))
    end = datetime.today()
    start = datetime.today()
    RSIlist = []
    dates = []
    i = 0

    #Creates recent business days according to timeframe and adds them to list
    while i < timeframe:
        start -= timedelta(days=1)
        if start.weekday() > 4:
            continue

        else:
            dates.append(start)
            i += 1


    try:
        df = web.DataReader(symbol, "yahoo",weekendEliminator(end, 2*timeframe), end)

    except:
        try:
            df = web.DataReader(symbol, "google", weekendEliminator(end, 2*timeframe), end)
        except:
            df = web.DataReader(symbol, "fred", weekendEliminator(end, 2*timeframe), end)


    #counts RSI for specific day and adds it to RSIlist
    for i in range(0, timeframe):
        ending = end - timedelta(days=timeframe-i)
        start = weekendEliminator(ending, timeframe)
        period = df[start:ending]
        RSIlist.append(RSI(period))
    plt.plot(dates, RSIlist)
    plt.show()

main()
