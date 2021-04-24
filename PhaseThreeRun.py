import pandas as pd
from SentimentProducer import SentimentProducer
from AssetLookUpTable.StockAssociation import StockAssociation
from WordUtils.Utils import Utils



class PhaseThreeRun:
    def __init__(self, directory):
        print("__________Load Old Df______________")
        df = pd.read_csv(directory)
        #print(df.columns)

        print("__________Post nuDf Creation___________")
        nuDf = StockAssociation().transformDf(50, df)

        print("Nudf Shape Before making surrounding transcript to string", nuDf.shape)

        nuDf['SurroudingWordsAsString'] = nuDf['SurroudingWords'].apply(Utils().vectorOfWordsToString)
        print("Nudf Shape After making surrounding transcript to string", nuDf.shape)
        # for index, row in nuDf.iterrows():
        #     print(row)



        # print("__________Semtiment Specific Tickers Producer___________")
        # print("BEFORE sentiement analysis shape is ", nuDf.shape)
        #df['Polarity']       = nuDf['SurroudingWords'].apply(SentimentProducer.getPolarity)
        nuDf['Subjectivity']  = nuDf['SurroudingWordsAsString'].apply(SentimentProducer.SentimentProducer.getSubjectivity)
        nuDf['Polarity']      = nuDf['SurroudingWordsAsString'].apply(SentimentProducer.SentimentProducer.getPolarity)
        nuDf['Analysis']      = nuDf['Polarity'].apply(SentimentProducer.SentimentProducer.getAnalysis)
        # print("AFTER sentiement analysis shape is ",nuDf.shape)
        # for index, row in nuDf.iterrows():
        #     print("Stock", row['Stock'], "Polarity", row['Polarity'], "Sentiment",  row['Analysis'])

        #
        print("__________Semtiment Producer___________")
        #df['Polarity']       = nuDf['Transcript'].apply(SentimentProducer.getPolarity)
        df['Subjectivity']  = df['Transcript'].apply(SentimentProducer.SentimentProducer.getSubjectivity)
        df['Polarity']      = df['Transcript'].apply(SentimentProducer.SentimentProducer.getPolarity)
        df['Analysis']      = df['Polarity'].apply(SentimentProducer.SentimentProducer.getAnalysis)
        # print("AFTER sentiement analysis shape is ",df.shape)
        # for index, row in df.iterrows():
        #     print("Search KeyWord:", row['SearchType'], "Polarity", row['Polarity'], "Sentiment",  row['Analysis'])
        self.specificTickerDF = nuDf
        self.generalSentiment = df
