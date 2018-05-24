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

if __name__ == '__main__':
    usdRates = OrderedDict()
    getRateHistory(SITE_URL + USD_SUFFIX, usdRates)
    with open("usd.json", 'w') as fp:
        json.dump(usdRates, fp)


    eurRates = OrderedDict()
    getRateHistory(SITE_URL + EUR_SUFFIX, eurRates)
    with open("euro.json", 'w') as fp:
        json.dump(eurRates, fp)

    numBins = len(list(usdRates.keys()))
    index = np.arange(numBins)
    fig, ax = plt.subplots()
    ax.bar(index, list(usdRates.values()), 0.4)
    ax.bar(index + 0.4, list(eurRates.values()), 0.4)
    ax.set_xticklabels(list(usdRates.keys()))
    ax.set_xticks(index + 0.4 / 2)
    ax.legend(['USD', 'EURO'])
    ax.grid()
    fig.tight_layout()
    plt.show()
