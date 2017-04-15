from datetime import *
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader as web

def averages(data):
    AVG_gain = 0
    AVG_loss = 0

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

    return AVG_gain, AVG_loss


#counts RSI for specific timeframe and date more info from RSI
#link: http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:relative_strength_index_rsi
def RSI(AVG_gain, AVG_loss):

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
    smoothRSI = []
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


    #gets the required course history

    try:
        df = web.DataReader(symbol, "yahoo", weekendEliminator(end, 250), end)

    except:
        try:
            df = web.DataReader(symbol, "google", weekendEliminator(end, 250), end)
        except:
            try:
                df = web.DataReader(symbol, "fred", weekendEliminator(end, 250), end)
            except:
                print("Course history couldn't been found for chosen stock. Please check for spelling.")
                main()


    #counts RSI for specific day and adds it to RSIlist
    gain, loss = averages(df[0:timeframe])
    i = timeframe +1
    close_prices = []
    print(gain, loss)

    for data in df[timeframe+1:].values:
        close = float(data[3])
        close_prices.append(close)

    gainlosses = [[]]
    for i in range(0, len(close_prices)-1):
        close1 = close_prices[i]
        close2 = close_prices[i+1]
        print(str(gain)+"   " +str(loss))
        gainloss = close2 - close1
        print("GAINLOSS: " + str(gainloss))

        if gainloss > 0:
            gain = (gain*(timeframe-1)+gainloss)/timeframe
            loss = loss*((timeframe-1)/timeframe)
        elif gainloss < 0:
            loss = (loss*(timeframe-1)-gainloss)/timeframe
            gain = gain*((timeframe-1)/timeframe)

        gain_loss = [gain, loss]
        print(gain_loss)
        gainlosses.append(gain_loss)

    for member in gainlosses[len(gainlosses)-timeframe:]:
        gain = member[0]
        loss = member[1]
        rsi = RSI(gain, loss)
        RSIlist.append(rsi)

    '''
    for date in dates:
        start = weekendEliminator(date, timeframe, "-")
        print(str(start) + "    " + str(date))
        period = df[start:date]
        rsi = RSI(period)
        RSIlist.append(rsi)
        print(rsi)

    '''
    plt.plot(list(reversed(dates)), RSIlist)
    #df[dates[len(dates)-1]:end]['Adj Close'].plot()
    plt.show()

main()
