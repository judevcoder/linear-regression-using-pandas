import pandas as pd
import numpy as np
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')
import statsmodels.formula.api as sm


df = pd.read_csv('USDT_BTC.csv', delimiter=';', header=0, names = ['date', 'high', 'low', 'close', 'volume', 'quote_volume', 'weighted_average'])
fig = plt.figure()

# define linear regression
def linreg(df):

    result = sm.ols(formula="timestamp ~ weighted_average", data=df).fit()
    return df
if __name__ == "__main":
    linreg()
