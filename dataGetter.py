from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from datetime import datetime
import json, re, pandas as pd


def getHTMLContent(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if isGoodResponse(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        print(f'Error during requests to {url} : {str(e)}')
        return None

def isGoodResponse(resp):
    '''
    Returns True if the response seems to be HTML, False otherwise
    '''
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 and content_type is not None and content_type.find('html') > -1)

def getPrice(url):
    """
    Returns a dict with dates and stock prices for the last 5 years
    Take input the link from where to download data
    """
    htmlContent = getHTMLContent(url)
    soup = BeautifulSoup(htmlContent, 'html.parser')
    soupData = soup.find_all('script', text=re.compile('afiseazaGrafic5Ani'))
    rawData = str(soupData)[str(soupData).find('afiseazaGrafic5Ani'):]

    data = str(rawData)[str(rawData).find('columns'):str(rawData).find('types')]
    dates = data[str(data).find('x')+4:str(data).find("['Close price")].replace("'", "").replace("\t", "").replace("\n", "").replace("\r", "")[:-2]
    goodDates = dates.split(",")

    prices = str(rawData)[str(rawData).find('Close price')+14:str(rawData).find('types')].replace("\t", "").replace("\n", "").replace("\r", "").replace("'", "").replace(" ", "").replace("]","")[:-2]
    goodPrices =  prices.split(",")
    goodPrices = [float(i) for i in goodPrices]

    dict_ = {'Dates': goodDates, 'Prices': goodPrices}
    print(len(dict_['Dates']), len(dict_['Prices']))
    return(dict_)

def getStockSymbols(url, save=True):
    '''
    Return a list with tickers from BVB.
    Saves JSON file with tickers
    '''
    htmlContent = getHTMLContent(URL)
    soup = BeautifulSoup(htmlContent, 'html.parser')
    soupData = soup.find_all('script', text=re.compile('listaCompanii'))
    rawData = str(soupData)[str(soupData).find('listaCompanii'):str(soupData).find('var widthCampCautare')]

    jsonData_ = json.loads(rawData
        .replace('listaCompanii = ', '')
        .replace('value', '"value"')
        .replace('label', '"label"')
        .replace('desc', '"desc"')
        .replace("\t", "")
        .replace("\n", "")
        .replace("\r", "")[:-3] + ']'
        )
    if save:
        with open('tickers.json', 'w') as jsonFile:
            json.dump(jsonData_, jsonFile)
    
    stockList= []
    for item in range(len(jsonData_)):
        stockList.append(jsonData_[item]['value'])
    return stockList
    

if __name__ == "__main__":
    URL = 'https://www.primet.ro/informatii-piata-cotatii-bursa?simbol=bvb'
    print(getStockSymbols(URL, False))


URL = 'https://www.primet.ro/informatii-piata-cotatii-bursa?simbol='

TICKERS = getStockSymbols(URL+'bvb', False)


dictList = {}
for ticker in TICKERS[:3]:
    url = URL + ticker
    print(f"Getting price for {ticker} from {url}")
    dictList[ticker] = getPrice(url)



url = URL + TICKERS[0]

htmlContent = getHTMLContent(url)
soup = BeautifulSoup(htmlContent, 'html.parser')
soupData = soup.find_all('script', text=re.compile('afiseazaGrafic5Ani'))
rawData = str(soupData)[str(soupData).find('afiseazaGrafic5Ani'):]

data = str(rawData)[str(rawData).find('columns'):str(rawData).find('types')]
dates = data[str(data).find('x')+4:str(data).find("['Close price")].replace("'", "").replace("\t", "").replace("\n", "").replace("\r", "")[:-2]
goodDates = dates.split(",")

prices = str(rawData)[str(rawData).find('Close price')+14:str(rawData).find('types')].replace("\t", "").replace("\n", "").replace("\r", "").replace("'", "").replace(" ", "").replace("]","")[:-2]
goodPrices =  prices.split(",")
goodPrices = [float(i) for i in goodPrices]

dict_ = {'Dates': goodDates, 'Prices': goodPrices}
print(len(dict_['Dates']), len(dict_['Prices']))
print(goodPrices)
print(dict_['Prices'])
