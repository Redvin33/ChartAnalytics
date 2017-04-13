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
    i = 0
    close_prices = []
    for info in data.values:
        close = float(info[3])
        close_prices.append(close)

    for i in range(0, len(close_prices)-1):
        close1 = close_prices[i]
        close2 = close_prices[i+1]

        gainloss = close2 - close1

        if gainloss > 0:
            AVG_gain += gainloss
        elif gainloss < 0:
            AVG_loss -= gainloss


    #print("AVG GAIN " + str(AVG_gain/i))
    #print("AVG LOSS " + str(AVG_loss/i))

    RS = AVG_gain/AVG_loss
    RSI = 100 - (100/(1+RS))

    return RSI

#Eliminates weekends because theyre not business days
def weekendEliminator(end, timeframe):
    i = 0
    while i < timeframe:
        end -= timedelta(days=1)
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
    i = 2

    #Creates recent business days according to timeframe and adds them to list
    while i < timeframe:
        start -= timedelta(days=1)
        if start.weekday() > 4:
            continue

        else:
            print(start)
            dates.append(start)
            i += 1
    print(len(dates))
    #gets the required course history
    try:
        df = web.DataReader(symbol, "yahoo",weekendEliminator(end, 2*timeframe+1), end)

    except:
        try:
            df = web.DataReader(symbol, "google", weekendEliminator(end, 2*timeframe+1), end)
        except:
            try:
                df = web.DataReader(symbol, "fred", weekendEliminator(end, 2*timeframe+1), end)
            except:
                print("Course history couldn't been found for chosen stock. Please check for spelling.")
                main()

    #counts RSI for specific day and adds it to RSIlist
    for i in range(2, timeframe):
        ending = weekendEliminator(end, i)
        start = weekendEliminator(ending, timeframe + 1)
        print(str(start) + "    " + str(ending))
        period = df[start:ending]
        RSIlist.append(RSI(period))
        print(RSI(period))
    plt.plot(dates, RSIlist)
    plt.show()

main()
