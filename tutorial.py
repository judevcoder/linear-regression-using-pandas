import pandas as pd
import matplotlib.pyplot as plt
from pandas import read_csv, DataFrame

Location = r'USDT_BTC.csv'
df = pd.read_csv(Location, delimiter=',', header=0, names=['date', 'high', 'low', 'close', 'volume', 'quote_volume', 'weighted_average'])