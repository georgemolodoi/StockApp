from dataGetter import *

def readCsv(file):
    with open(file, 'r') as f:
        reader = csv.reader(f, delimiter=";")
        tickers = list(reader)

    return tickers[0]

URL = 'https://www.primet.ro/informatii-piata-cotatii-bursa?simbol='
TICKERS = readCsv('tickerError.csv')


NOdata = []
ProblemParisng = []
for ticker in TICKERS:
    url = URL+ticker
    htmlContent = getHTMLContent(url)
    soup = BeautifulSoup(htmlContent, 'html.parser')
    soupData = soup.find_all('script', text=re.compile('afiseazaGrafic5Ani'))
    rawData = str(soupData)[str(soupData).find('afiseazaGrafic5Ani'):]

    data = str(rawData)[str(rawData).find('columns'):str(rawData).find('types')]
    dates = data[str(data).find('x')+4:str(data).find("['Close price")].replace("'", "").replace("\t", "").replace("\n", "").replace("\r", "").replace(" ", "")[:-2]
    goodDates = dates.split(",")

    prices = str(rawData)[str(rawData).find('Close price')+14:str(rawData).find('types')].replace("\t", "").replace("\n", "").replace("\r", "").replace("'", "").replace(" ", "").replace("]","")
    goodPrices =  prices.split(",")
    
    dict_ = {'Dates': goodDates, 'Prices': goodPrices}

    if len(dict_['Dates']) != len(dict_['Prices']):
        ProblemParisng.append(ticker) 

    if len(soupData) == 0:
        print('*'*15)
        print(ticker) 
        NOdata.append(ticker)
        

print(len(NOdata) + len(ProblemParisng))
print(len(TICKERS))



