import pandas as pd
from InternetScraper.WebCrawler import WebCralerSearch
from InternetScraper.ScrapeVideo import ScrapeVideos
from WordUtils.Utils import Utils
from datetime import datetime
from collections import defaultdict



class PhaseOneRun:
    def __init__(self, cryptoSpecificsSearch, stockSpecificsSearch, searchPhrases):


        allLinks=[]
        dict_searchPhrase_links = defaultdict(list)

        #######SETCTION 1 Gets links of youtube videos videos to scrape###########
        for searchThis in searchPhrases:
            links    = WebCralerSearch(searchThis,10).getResults()
            dict_searchPhrase_links[searchThis] = dict_searchPhrase_links[searchThis] + links

            allLinks = allLinks + links

        #print(type( allLinks), "AllLinks:", allLinks)

        #######SETCTION 2 GETS TRANSCRIPTS OF VIDEOS FROM LINKS#######
        #dictOfTranscripts = ScrapeVideos().getTranscipts(allLinks)
        for k, v in dict_searchPhrase_links.items():
            dict_searchPhrase_links[k] = ScrapeVideos().getTranscipts(v)

        # Test Print
        # for k, v in dictOfTranscripts.items():
        #     print(k,v)


        #df = pd.DataFrame.from_dict(dictOfTranscripts, orient='index')

        df = pd.DataFrame(columns= ['YoutubeID', 'Transcript', 'SearchType'])
        for searchPhrase, dictionary in dict_searchPhrase_links.items():
            for youTubeID, transcript in dictionary.items():
                df.loc[len(df.index)] = [youTubeID, transcript, searchPhrase]

        print("__________DF PRINT______________")
        print(df.shape)
        print(df)
        #

        df['VectorOfWords'] = df['Transcript'].apply(Utils().vectorOfWords)
        print("__________DF PRINT______________")
        print(df.shape)
        print(df)
        #
        #
        # """This Proccess is to save time in the development proccess
        # So there isn't a need to scape youtube everytime we want to test
        # and refine sentiment producing functions. Undecided if this will be saved for later"""
        #
        print("__________SAVE DF to CSV______________")
        now = datetime.now()
        #print("now =", now) #Test Print
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
        print("date and time =", dt_string) #Test Print
        directory = "OldData/"
        df.to_csv(directory + dt_string +".csv")

        #
        #
        # print("__________Post nuDf Creation___________")
        # nuDf = StockAssociation().transformDf(50, df)
        # nuDf['SurroudingWordsAsString'] = nuDf['SurroudingWords'].apply(Utils().vectorOfWordsToString)
        # print(nuDf)
        #

