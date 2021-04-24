import pandas as pd
from SentimentProducer import SentimentProducer
from InternetScraper.WebCrawler import WebCralerSearch
from InternetScraper.ScrapeVideo import ScrapeVideos
from AssetLookUpTable.StockAssociation import StockAssociation
from WordUtils.Utils import Utils
from PhaseOneRun import PhaseOneRun


class run:
    def __init__(self, cryptoSpecificsSearch, stockSpecificsSearch, searchPhrases):
        mostRecentScrape = PhaseOneRun(cryptoSpecificsSearch, stockSpecificsSearch, searchPhrases)





# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    cryptoSpecificsSearch = ["Ehteurum", "Cardano", "Bitcoin", "chainlink",  "polkadot"]

    stockSpecificsSearch = ["GME", "AAPL", "MSFT", "TSLA"]

    searchPhrases = ["meme+stock","meme+stock+market", "meme+stock+trading", "stock+market", "nasdaq"]+stockSpecificsSearch#"sp500", "russell+2000" ]

