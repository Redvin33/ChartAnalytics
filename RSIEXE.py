from yahoo_finance import *
from datetime import *

def RSI(data):
    AVG_gain = 0
    AVG_loss = 0

    for info in data:
        open = float(info['Open'])
        close = float(info['Close'])
        gainloss = close-open
        if gainloss > 0:
            AVG_gain += gainloss
        elif gainloss < 0:
            AVG_loss -= gainloss


    RS = AVG_gain/AVG_loss

    RSI = 100 - (100/(1+RS))
    print(RSI)
    return


def main():
    symbol = input("Write symbol of the stock: ")
    timeframe = int(input("Choose dayrange: "))
    share = Share(symbol)
    date = (datetime.today() - timedelta(days=timeframe)).strftime('%Y-%m-%d')
    data = share.get_historical(date, datetime.today().strftime('%Y-%m-%d'))
    RSI(data)

main()
