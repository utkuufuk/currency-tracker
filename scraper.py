from collections import OrderedDict
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import argparse
import requests
import re
import json

AGENT = "Mozilla/5.0 Chrome/47.0.2526.106 Safari/537.36"
SITE_URL = "https://tr.investing.com/currencies/"
USD_SUFFIX = "usd-try-historical-data"
EUR_SUFFIX = "eur-try-historical-data"
GAU_SUFFIX = "gau-try-historical-data"
GAU_SCALE = 35

def createSoup(url):
    return BeautifulSoup(requests.get(url, headers={"User-Agent": AGENT}).text, "lxml")

def getRateHistory(url, rates):
    page = createSoup(url)
    resultBox = page.find('table', {'class':'historicalTbl'})
    for row in resultBox.findAll('tr'):
        columns = row.findAll('td')
        if len(columns) == 0:
            continue
        date = columns[0].getText()
        rate = columns[1].getText()
        rates[date] = float(rate.replace(',', '.'))

# fetch USD history
usdRates = OrderedDict()
getRateHistory(SITE_URL + USD_SUFFIX, usdRates)
with open("usd.json", 'w') as fp:
    json.dump(usdRates, fp)
print("Fetched USD history.")

# fetch EUR history
eurRates = OrderedDict()
getRateHistory(SITE_URL + EUR_SUFFIX, eurRates)
with open("eur.json", 'w') as fp:
    json.dump(eurRates, fp)
print("Fetched EUR history.")

# fetch GAU history
gauRates = OrderedDict()
getRateHistory(SITE_URL + GAU_SUFFIX, gauRates)
with open("gau.json", 'w') as fp:
    json.dump(gauRates, fp)
print("Fetched GAU history.")

# fix date order
usdRates = OrderedDict(reversed(usdRates.items()))
eurRates = OrderedDict(reversed(eurRates.items()))
gauRates = OrderedDict(reversed(gauRates.items()))

# plot historical data
dates = list(usdRates.keys())
lbl = "GAU (x" + str(GAU_SCALE) + ")"
fig, ax = plt.subplots()
x = range(0, len(dates)) 
ticks = [date[:5] for date in dates]
plt.xticks(x, ticks)
ax.plot(x, list(eurRates.values()), color='green', label="EUR")
ax.plot(x, [val / GAU_SCALE for val in list(gauRates.values())], color='orange', label=lbl)
ax.plot(x, list(usdRates.values()), color='blue', label="USD")
ax.legend()
ax.grid()
fig.tight_layout()
plt.show()
