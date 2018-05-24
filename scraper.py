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
BAR_WIDTH = 0.25

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

# fetch EURO history
eurRates = OrderedDict()
getRateHistory(SITE_URL + EUR_SUFFIX, eurRates)
with open("euro.json", 'w') as fp:
    json.dump(eurRates, fp)

# reverse the date order
usdRates = OrderedDict(reversed(usdRates.items()))
eurRates = OrderedDict(reversed(eurRates.items()))

# plot the historical data
numBins = len(list(usdRates.keys()))
xIndices = np.arange(numBins)
fig, ax = plt.subplots()
ax.bar(xIndices, list(usdRates.values()), BAR_WIDTH, label="USD")
ax.bar(xIndices + BAR_WIDTH, list(eurRates.values()), BAR_WIDTH, label="EURO")
ax.set_xticklabels([label[:-5] for label in list(usdRates.keys())])
ax.set_xticks(xIndices + BAR_WIDTH / 2)
ax.legend()
ax.grid()
fig.tight_layout()
plt.axis([0, numBins, 3, 6])
plt.show()
