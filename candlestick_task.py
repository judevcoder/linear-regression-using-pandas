# import warnings
# import matplotlib.cbook
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# import datetime as dt
# from matplotlib.finance import candlestick_ohlc
# import matplotlib.ticker as mticker
#
# Location = r'philipp/BTC_DASH.csv'
# df = pd.read_csv(Location, delimiter=';', header=0, names=['date', 'high', 'low', 'close', 'volume', 'quote_volume','weighted_average'])
#
#
# #Reset the index to remove Date column from index
# df_ohlc = df.reset_index()
#
# #Naming columns
# df_ohlc.columns = ["Index","Date","High",'Low',"Close", "Volume", "Quote_volume", "Weighted_average"]
#
# #Converting dates column to float values
# df_ohlc['Date'] = df_ohlc['Date'].map(mdates.datestr2num)
#
# #Making plot
# fig = plt.figure()
# ax1 = plt.subplot2grid((6,1), (0,0), rowspan=6, colspan=1)
#
# #Converts raw mdate numbers to dates
# ax1.xaxis_date()
# plt.xlabel("Date")
# print(df_ohlc)
#
# #Making candlestick plot
# candlestick_ohlc(ax1,df_ohlc.values,width=1, colorup='g', colordown='k',alpha=0.75)
# plt.ylabel("Price")
# plt.legend()
#
# plt.show()

import datetime
import matplotlib.pyplot as plt

x = ['Mon Sep 1 16:40:20 2015', 'Mon Sep 1 16:45:20 2015',
    'Mon Sep 1 16:50:20 2015', 'Mon Sep 1 16:55:20 2015']
y = range(4)

x = [datetime.datetime.strptime(elem, '%a %b %d %H:%M:%S %Y') for elem in x]

(fig, ax) = plt.subplots(1, 1)
ax.plot(x, y)
plt.show()