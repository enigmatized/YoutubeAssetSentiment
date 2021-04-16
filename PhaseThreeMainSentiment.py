import pandas as pd
from ScrapeVideo import ScrapeVideo
from SentimentProducer import SentimentProducer
import json
from collections import defaultdict
from WebCrawler import WebCralerSearch
from ScrapeVideo import ScrapeVideos
from StockAssociation import StockAssociation
from Utils import Utils
from datetime import datetime
from LookUpTable import LookUpTable


if __name__ == '__main__':
    print("__________Load Old Df______________")
    df = pd.read_csv("OldData/04_04_2021_12_09_55.csv")

    print("__________Post nuDf Creation___________")
    nuDf = StockAssociation().transformDf(50, df)

    print("Nudf Shape Before making surrounding transcript to string", nuDf.shape)

    nuDf['SurroudingWordsAsString'] = nuDf['SurroudingWords'].apply(Utils().vectorOfWordsToString)
    print("Nudf Shape After making surrounding transcript to string", nuDf.shape)
    # for index, row in nuDf.iterrows():
    #     print(row)



    print("__________Semtiment Producer___________")
    print("BEFORE sentiement analysis shape is ", nuDf.shape)
    #df['Polarity']       = nuDf['SurroudingWords'].apply(SentimentProducer.getPolarity)
    nuDf['Subjectivity']  = nuDf['SurroudingWordsAsString'].apply(SentimentProducer.getSubjectivity)
    nuDf['Polarity']      = nuDf['SurroudingWordsAsString'].apply(SentimentProducer.getPolarity)
    nuDf['Analysis']      = nuDf['Polarity'].apply(SentimentProducer.getAnalysis)
    print("AFTER sentiement analysis shape is ",nuDf.shape)
    for index, row in nuDf.iterrows():
        print("Stock", row['Stock'], "Polarity", row['Polarity'], "Sentiment",  row['Analysis'])




