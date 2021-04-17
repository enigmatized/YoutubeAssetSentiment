from collections import defaultdict
import json
import re
import pandas as pd
from coinmarketcap import Market
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from pyrh import Robinhood
import requests
import csv
from datetime import datetime






"""This class creates a dictionary/look up talbe of company names and stock ticker symbols
This is used to scan transcripts to find where ticker symbols/company names were mentioned
Then it takes a"""
class LookUpTable:

    def __init__(self, new = True):
        self.lookUpByCompany       = None
        self.lookUpBySymbol        = None
        self.lookUpBySymbol4Sector = None #TODO Fill This out better

        #TODO FILL IN PASSWORD OR SEPERATE FILE TO LOAD FROM
        self.RobinHoodUser     = None
        self.RobinHoodPassword = None


        if new:
            #Dictionary Loading
            self.localJsonData()
            print("After local JsonLoad Look table length:", len(self.lookUpBySymbol))
            self.getNasdaqSymbols()
            print("After Nassaq Look table length:", len(self.lookUpBySymbol))
            # # self.addYahooMovers()
            # # print("After YahooMovers Look table length:", len(self.lookUpBySymbol))
            self.addFinnHub()
            print("After FinHub Look table length:", len(self.lookUpBySymbol))
            # #self.addRobinhood()
            #print("Printing Dictionary LookupBySymbol", self.lookUpBySymbol) #Test Print
            #self.getCryptSymbols()
            #print("Crypto Added successfully")#Test Print
            self.writeDictToFile(self.lookUpBySymbol, "lookUpBySymbol")
            #self.writeDictToFile(self.lookUpByCompany, "lookUpByCompany")

        else:
            self.loadLookupTable()


    """Function to add crypto symbols and names to look up table
    Note using CoinMarketCap with API
    """



    def localJsonData(self):
        f = open('../TickerSymbols/tickerCompany.json')
        self. data = json.load(f)
        f.close()

        lookupbySymbol          = defaultdict(int)
        lookupbycompany         = defaultdict(int)
        lookupbySymbolForSector = defaultdict(int)


        for dictionary in self.data:
            lookupbycompany[dictionary['Name']]  = dictionary['Symbol']
            lookupbySymbol[dictionary['Symbol']] = dictionary['Name']
            lookupbySymbolForSector[dictionary['Symbol']] = dictionary['Sector']

        self.lookUpByCompany = lookupbycompany
        self.lookUpBySymbol = lookupbySymbol
        self.lookUpBySymbol4Sector = lookupbySymbolForSector


    def getCryptSymbols(self):

        #url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
        parameters = {
            'start': '1',
            'limit': '5000',
            'convert': 'USD'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '3f97024f-1495-4935-842b-d56de15a21d1',
        }

        session = Session()
        session.headers.update(headers)

        try:
            #response = session.get(url, params=parameters)
            response = session.get(url)
            data = json.loads(response.text)
            #print(data)
            #print(type(data))
            for dat in data['data']:
                self.lookUpByCompany[dat['name']] = dat['symbol']
                self.lookUpBySymbol[dat['symbol']] = dat['name']


        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)


    def getNasdaqSymbols(self):
        df = pd.read_csv('../TickerSymbols/nasdaq_screener_1616809987539.csv')
        for index, row in df.iterrows():
            compName = row['Name']
            symbol   = row['Symbol']
            try:
                compName.replace(' Common Stock','')
            except:
                print(" Common Stock not in name")
                compName = row['Name']

            if self.lookUpByCompany[compName] == 0:
                self.lookUpByCompany[compName] = row['Symbol']
            if self.lookUpBySymbol[row['Symbol']] == 0:
                self.lookUpBySymbol[row['Symbol']] = compName


    def addYahooMovers(self):
        import requests
        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-movers"

        querystring = {"region": "US", "lang": "en-US", "start": "0", "count": "6"}

        headers = {
            'x-rapidapi-key': "5174823edbmshba11cc25ca448c1p1a0f92jsn6479ae7852f8",
            'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        print(response.text)

    def addRobinhood(self):
        rh = Robinhood()
        if self.RobinHoodUser:

            rh.login(username=self.RobinHoodUser, password=self.RobinHoodPassword)
            rh.print_quote("AAPL")
        else: print("You must set your Robinhood passwords up in init")

    def addFinnHub(self):
        token = 'c1l4b6a37fko6in50d9g'
        r = requests.get('https://finnhub.io/api/v1/stock/symbol?exchange=US&token='+ token)
        #print(r.json())#Test Print
        json_data = json.loads(r.text)
        #print(type(json_data))#Test Print
        for x in json_data:
            compName = x['description']
            symbol   = x['symbol']

            if self.lookUpByCompany[compName] == 0:
                self.lookUpByCompany[compName] = symbol
            if self.lookUpBySymbol[symbol] == 0:
                self.lookUpBySymbol[symbol] = compName


    def writeDictToFile(self,d, types):
        now = datetime.now()
        #dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
        dt_string = ""

        with open(dt_string +types+".csv", "w", newline="") as outfile:
            w = csv.writer(outfile)
            for key, val in d.items():
                w.writerow([key, val])


    def loadLookupTable(self):
        with open('../lookUpBySymbol.csv', mode='r') as infile:
            reader = csv.reader(infile)
            mydict = {rows[0].lower(): rows[1].lower() for rows in reader}

        #mydict = csv.DictReader(open("lookUpBySymbol.csv"))
        #print(mydict, len(mydict))
        self.lookUpBySymbol = defaultdict(int, mydict)
        print("Length of self.lookUpBySymbol after Loading", len(self.lookUpBySymbol))
        # for k, v in self.lookUpBySymbol.items():
        #     print(k, v)

if __name__ == "__main__":
    #LookUpTable(new=True)
    hasAMC = ""
    for k, v in LookUpTable(new=False).lookUpBySymbol.items():
        print(k, v)
        if k.lower() == "amc":
            hasAMC = k+v
    print(hasAMC)
    print(LookUpTable(new=False).lookUpBySymbol['llllllllllllllll'])