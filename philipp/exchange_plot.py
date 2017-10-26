import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc
import numpy as np
import urllib
import datetime as dt
def bytespdate2num(fmt, encoding='utf-8'):#Datumsformat Konverter
	strconverter = mdates.strpdate2num(fmt)
	def bytesconverter(b):
		s = b.decode(encoding)
		return strconverter(s)
	return bytesconverter

def graph_data(stock):
	fig = plt.figure()
	ax1 = plt.subplot2grid((1,1), (0,0))
	stock_price_url = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range=10d/csv'
	source_code = urllib.request.urlopen(stock_price_url).read().decode()
	stock_data = []#
	split_source = source_code.split('\n')#split by new line
	for line in split_source:
		split_line = line.split(',')
		if len(split_line) ==6:		#header weghauen wenn 6 elemente mit komma getrennt sind gehts los
			if 'values' not in line and 'labels' not in line:
				stock_data.append(line)
	date, closep, highp, lowp, openp, volume = np.loadtxt(stock_data,delimiter=',',unpack=True,converters={0: bytespdate2num('%Y%m%d')})#%Y-%m-%d-%H-%M-%S
	x = 0
	y = len(date)
	ohlc =  []
	while x < y:
		append_me = date[x], closep[x], highp[x], lowp[x], openp[x], volume[x]
		ohlc.append(append_me)
		x+=1
	candlestick_ohlc(ax1, ohlc, width=0.4, colorup='green', colordown='red')
	#ax1.plot_date(date, closep,'-', label='Price')
	#ax1.fill_between(date, closep, 0, where=(closep>closep[0]), facecolor='g', alpha=0.3) #anstelle 0 Kaufpreis oder close[10] eingeben filllevel start nach oben und unten
	for label in ax1.xaxis.get_ticklabels():#Beschriftung drehen
		label.set_rotation(45)
		ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))	#datum umformatieren
		ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))#immer 10 sklaenteile sind beschrifttet auch mit zoom x-achse
		ax1.xaxis.label.set.color('blue')#axis label farbwechsel ax1.set_yticks([0,10,20,30,40]) # yskala festlegen
		ax1.grid(True, color='g', linestyle='-',linewidth=0.3) # Gitter im plot
		plt.xlabel('Date')
		plt.ylabel('Price')
		plt.title(stock)
		plt.legend()
		plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
		plt.show()


graph_data('ebay')
