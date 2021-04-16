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




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    """
    TODO So this function seems to be random.
    Sometimes the elements tags work and do not work.
    I want to create a loop where if it fails mid proccess, It re-try's 
    till it successeds oe fails 10x. If it fails more 10x then there is something
    wrong on this side
    """
    searchPhrases = ["meme+stock", "stock", "GME", "Cardano", "polkadot"]

    allLinks=[]
    for searchThis in searchPhrases:
        links    = WebCralerSearch(searchThis,8).getResults()
        allLinks = allLinks + links
    print("AllLinks:", allLinks)
    dictOfTranscripts = ScrapeVideos().getTranscipts(allLinks)

    # Test Print
    # for k, v in dictOfTranscripts.items():
    #     print(k,v)


    #df = pd.DataFrame.from_dict(dictOfTranscripts, orient='index')

    df = pd.DataFrame(columns= ['YoutubeID', 'Transcript'])
    for k,v in dictOfTranscripts.items():
        df.loc[len(df.index)] = [k, v]

    print("__________DF PRINT______________")
    print(df.shape)
    print(df)


    df['VectorOfWords'] = df['Transcript'].apply(Utils().vectorOfWords)
    print("__________DF PRINT______________")
    print(df.shape)
    print(df)


    """This Proccess is to save time in the development proccess
    So there isn't a need to scape youtube everytime we want to test
    and refine sentiment producing functions. Undecided if this will be saved for later"""

    print("__________SAVE DF to CSV______________")
    now = datetime.now()
    #print("now =", now) #Test Print
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    print("date and time =", dt_string) #Test Print
    directory = "OldData/"
    df.to_csv(directory + dt_string +".csv")



    print("__________Post nuDf Creation___________")
    nuDf = StockAssociation().transformDf(50, df)
    nuDf['SurroudingWordsAsString'] = nuDf['SurroudingWords'].apply(Utils().vectorOfWordsToString)
    print(nuDf)




    print("__________Semtiment Producer___________")
    print(nuDf.shape)
    #df['Polarity']       = nuDf['SurroudingWords'].apply(SentimentProducer.getPolarity)
    nuDf['Subjectivity']  = nuDf['SurroudingWordsAsString'].apply(SentimentProducer.getSubjectivity)
    nuDf['Polarity']      = nuDf['SurroudingWordsAsString'].apply(SentimentProducer.getPolarity)
    nuDf['Analysis']      = nuDf['Polarity'].apply(SentimentProducer.getAnalysis)
    for index, row in nuDf.iterrows():
        print("Stock", nuDf['Stock'], "Polarity", nuDf['Polarity'], "Sentiment",  row['Analysis'])



    #df['Subjectivity']  = df['Transcript'].apply(SentimentProducer.getSubjectivity)
    #df['Polarity']      = df['Transcript'].apply(SentimentProducer.getPolarity)





    # dictOfTranscripts  = ScrapeVideo().getTranscriptByLink('fttA-rNRYG4')
    # print("dictOfTranscripts", dictOfTranscripts)
    #
    # df.loc[len(df)]    = dictOfTranscripts+[None]
    # dictOfTranscripts  = ScrapeVideo().getTranscriptByLink('wYRyBX2xjR8')
    # df.loc[len(df)]    = dictOfTranscripts + [None]
    # df['Subjectivity'] = df['transcript'].apply(SentimentProducer.getSubjectivity)
    # df['Polarity']     = df['transcript'].apply(SentimentProducer.getPolarity)
    #




