import pandas as pd
from SentimentProducer import SentimentProducer
from InternetScraper.WebCrawler import WebCralerSearch
from InternetScraper.ScrapeVideo import ScrapeVideos
from AssetLookUpTable.StockAssociation import StockAssociation
from WordUtils.Utils import Utils


# Press the green button in the gutter to run the script.
if __name__ == '__main__':


    searchPhrases = ["meme+stock", "stock", "GME"]

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




