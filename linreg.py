# -*- coding: utf-8 -*-
from __future__ import print_function
# General syntax to import specific functions in a library:
#from (library) import (specific library function)
#import (library) as (give the library a nickname/alias)
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')
#style.use('ggplot')
import pandas as pd #this is how I usually import pandas
import statsmodels.api as sm #für lineare regression
from statsmodels.sandbox.regression.predstd import wls_prediction_std
from patsy import dmatrices
import numpy as np #calculate with time
import sys
import functools #für die identifikation der Handelssignale bolean
from _functools import partial, reduce #für die identifikation der Handelssignale bolean
import datetime


Location = r'USDT_BTC.csv'
df = pd.read_csv(Location, delimiter=';', header=0, names=['date', 'high', 'low', 'close', 'volume', 'quote_volume','weighted_average'])#df datenframe sollten wir später nach USDT_BTC umbenennen

x = df.date
y = df.weighted_average

x = [datetime.datetime.strptime(elem, '%Y-%m-%d %H:%M:%S') for elem in x]
(fig, ax) = plt.subplots(1, 1)
ax.plot(x, y)
plt.show()

# def start_end_point():
#Datei einlesen/read file
# convert string to date type
datetime_date = []
for string_date in df.date:
	datetime_str = datetime.datetime.strptime(string_date, "%Y-%m-%d %H:%M:%S")
	datetime_date.append(datetime_str)

# convert date to float type
timelines = []
for timestamp in datetime_date:
	datetime_float = 10000*timestamp.year + 100*timestamp.month + timestamp.day + 0.01*timestamp.hour + 0.0001*timestamp.minute + 0.000001*timestamp.second
	timelines.append(datetime_float)

df['timecalc'] = timelines

# getting index for start and end point
df1 = df.loc[0:8640, ['timecalc', 'weighted_average']]
timelines_max = max(i for i in timelines if i > 0)
timelines_min = min(i for i in timelines if i > 0)

timelines_max_index = timelines.index(timelines_max)
timelines_min_index = timelines.index(timelines_min)

# getting start and end points

start_point = {
	'start_date':df.date[timelines_min_index],
	'weighted_average':df.weighted_average[timelines_min_index],
	'high':df.high[timelines_min_index],
	'low':df.low[timelines_min_index],
	'close':df.close[timelines_min_index],
	'volume':df.volume[timelines_min_index],
	'quote_volume':df.quote_volume[timelines_min_index]
}
end_point = {
	'end_date':df.date[timelines_max_index],
	'weighted_average':df.weighted_average[timelines_max_index],
	'high':df.high[timelines_max_index],
	'low':df.low[timelines_max_index],
	'close':df.close[timelines_max_index],
	'volume':df.volume[timelines_max_index],
	'quote_volume':df.quote_volume[timelines_max_index]
}
# 	return start_point, \
# 		   end_point
# if __name__ == "__main__":
# 	print(start_end_point())


# df1 = df.loc[0:8640,['timecalc', 'weighted_average']] #dataframe für die zu erstellende Matrix 1 Monat 8640 Werte / Dataframe for the matrix to be created 1 month 8640 values
df1.fillna(method='pad') #missing values mit dem vorherigem Wert auffüllen / Fill missing values with the previous value

# def linreg(df1):
y, X = dmatrices('weighted_average ~ timecalc', data=df1, return_type='dataframe') #Matrix für die Lineare regression erzeugen / Matrix for the linear regression
mod = sm.OLS(y,X) #modelliere
res = mod.fit() #fitten#dataframe für die zu erstellende Matrix 1 Monat 8640 Werte / Dataframe for the matrix to be created 1 month 8640 values
intercept = res. params.get_value(0)#Schnittpunkt auslesen / Reading the intersection point
slope = res.params.get_value(1)#Anstieg auslesen / Increse read out
streu = res.resid.std() #standardabweichung berechnen / standard deviation
df1['linreg_1m']=slope*df1['timecalc']+intercept #lineare regressionsgerade schreiben / Write linear regression line
df1['std_plus'] = df1['linreg_1m']+streu #streubereich festlegen und schreiben / And write
df1['std_minus'] = df1['linreg_1m']-streu
	# return df1
# print(df1)
# if __name__ == "__main":
# 	linreg(df1)

#res.summary()
#res.rsquared
#res.params
#res.resid
#res.resid.std()
#dir(res)


# it works up to here
#now I want that code inside of a function, where i can define frequency and frame/window, I want to use it in a rolling funktion
#wäre toll wenn ich hier einfach frequeenz und window einstellen könnte / Would be great if I simply here frequeenz and window adjust could

#Lineare Regression rolling mit Funktion /Linear regression rolling with function
#
# df1.fillna(method='pad')#missing values mit dem vorherigem Wert auffüllen
# def linreg(df1):
# 	y, X = dmatrices('weighted_average ~ timecalc',data=df1,return_type='dataframe')#Matrix für die Lineare regression erzeugen
# 	mod=sm.OLS(y,X)#modelliere
# 	res=mod.fit()#fitten
# 	intercept = res.params.get_value(0)#Schnittpunkt auslesen
# 	slope = res.params.get_value(1)#Anstieg auslesen
# 	streu = res.resid.std() #standardabweichung berechnen
# 	df1['linreg_1m']=slope*df1['timecalc']+intercept #lineare regressionsgerade schreiben
# 	df1['std_plus'] = df1['linreg_1m']+streu #streubereich festlegen und schreiben
# 	df1['std_minus'] = df1['linreg_1m']-streu
# 	return df1
# df[['linreg_1m'],['std_plus'],['std_minus']] = pd.rolling_apply(df1['timecalc'],df1['weighted_average'],window=8640,linreg())




# #try and error
# r=df1.rolling(window=8640,freq=2160).linreg()#rolling funktion für time series
# df1=r#r.sum() usw auch möglich
# #
# df['new_column'] = df.apply(lambda x: linreg(x['High'],x['Low'],x['Close']), axis=1)
#
#
# #Anzeigen der dataframes
# df.loc[197999:198020,['linreg_1m']]
#
#
#
#
#
#
#
# #altes zeug funktioniert auch nur mit window frequenz leider nicht / Old tool also works only with windowfrequenz unfortunately not
#
# #Lineare Regression selbst berechnet / Linear regression calculated itself
# frame = 12 #Anzahl der zu berücksichtigenden Werte rolling wahrscheinlich ungeeignet / Number of values to be considered probably not suitable
#   #hier müssen noch eine Menge Bedingungen und dynamisch Zeitfenster ausgetüftelt werden / Here a lot of conditions and dynamic time windows have to be worked out
# df['timecalc'] = df.index #Lineare Regression, mit dem Index rechnen
# timecalc = df['timecalc'] #Achtung möglicher workaround
# r = timecalc.rolling(window=frame) #Bildung der benötigten Summen mit der rolling funktion
# sumt = r.sum()
# timecalc = timecalc*timecalc
# r = timecalc.rolling(window=frame)
# sumtsq = r.sum()
# timecalc = df['weighted_average']
# r = timecalc.rolling(window=frame)
# sumwa = r.sum()
# timecalc = df['']*df['weighted_avtimecalcerage']
# r = timecalc.rolling(window=frame)#freq='W' weekly, 'D' dayly, '2h20min' offset, wie oft wird ausgeführt-offset aliases
# sumtwa = r.sum()
# #Formel für die lineare Regression
# df['mreg'] = ((frame*sumtwa) - (sumt * sumwa)) / ((frame*sumtsq) - (sumt**2)) # Anstieg der linearen Regression
# df['linreg_1h'] = (df['timecalc']*((frame*sumtwa) - (sumt * sumwa)) / ((frame*sumtsq) - (sumt**2))) + (((sumtsq * sumwa) - (sumt * sumtwa)) / ((frame * sumtsq) - sumt**2))
# #ich weiss nicht ob so viele Klammern notwendig sind, ober von rechts nach links ausführt oder die Regeln beachtet
#
# #Lineare Regression 1 Monat wird wöchnetlich neu berechnet
# frame = 8640 #12x24x30=8640 Anzahl der zu berücksichtigenden Werte / hier müssen noch eine Menge Bedingungen und dynamisch Zeitfenster ausgetüftelt werden
# df['timecalc'] = df.index #Lineare Regression, mit dem Index rechnen
# timecalc = df['timecalc'] #Achtung möglicher workaround
# r = timecalc.rolling(window=frame,freq='W') #Bildung der benötigten Summen mit der rolling funktion
# sumt = r.sum()
# timecalc = timecalc*timecalc
# r = timecalc.rolling(window=frame,freq='W')
# sumtsq = r.sum()
# timecalc = df['weighted_average']
# r = timecalc.rolling(window=frame,freq='W')
# sumwa = r.sum()
# timecalc = df['timecalc']*df['weighted_average']
# r = timecalc.rolling(window=frame,freq='W')#freq='W' weekly, 'D' dayly, '2h20min' offset, wie oft wird ausgeführt-offset aliases
# sumtwa = r.sum()
# #Formel für die lineare Regression
# df['mreg_m'] = ((frame*sumtwa) - (sumt * sumwa)) / ((frame*sumtsq) - (sumt**2)) # Anstieg der linearen Regression Monat
# df['linreg_1m'] = (df['timecalc']*((frame*sumtwa) - (sumt * sumwa)) / ((frame*sumtsq) - (sumt**2))) + (((sumtsq * sumwa) - (sumt * sumtwa)) / ((frame * sumtsq) - sumt**2))
# #ich weiss nicht ob so viele Klammern notwendig sind, ober von rechts nach links ausführt oder die Regeln beachtet