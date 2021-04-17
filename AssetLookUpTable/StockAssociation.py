from collections import defaultdict
import re
import pandas as pd
from AssetLookUpTable.LookUpTable import LookUpTable






"""This class creates a dictionary/look up talbe of company names and stock ticker symbols
This is used to scan transcripts to find where ticker symbols/company names were mentioned
Then it takes a"""


class StockAssociation:

    def __init__(self, reLoadLookUpTable = False):
        self.LookUpTable = LookUpTable(reLoadLookUpTable)
        self.lookUpBySymbol = self.LookUpTable.lookUpBySymbol




    def createListOfWords(self, string):
        wordList = re.sub("[^\w]", " ", string).split()
        return wordList


    def transformDf(self, num, df):
        nuDf =  pd.DataFrame(columns= ['Stock', 'SurroudingWords'])
        convert = defaultdict(list)
        #Iterates through each row, using the vector of words
        #to
        for index, row in df.iterrows():
            #print("type(row['VectorOfWords'])", type(row['VectorOfWords']))
            ls = eval(row['VectorOfWords'])#TODO this is the holly Grail of no-no's.
            #Creates a list of word

            dictionary = self.numWords(num, ls)#Why would this return a dictionary
            if len(dictionary)> 0: print(dictionary)
            for k,  v in dictionary.items():
                convert[k] =  convert[k]+ v


        nuDf = pd.DataFrame(list(convert.items()), columns= ['Stock', 'SurroudingWords'])
        #nuDf = pd.DataFrame.from_dict(convert,columns= ['Stock', 'SurroudingWords'] )
        return nuDf




    """Takes in amount of words you want surounding company name
    Also takes in the transcript by vector of words"""
    def numWords(self, num, vectorOfWords):
        """Return s dictionary where K is and Value is"""

        #TODO MAJOR CHANGE NEEDS TO BE DONE ON THE DATA STRUCTURES HERE
        #What if I have duplicates in the dictionary key
        #As of now I just merge list
        company = defaultdict(list)
        for i in range(0, len(vectorOfWords)-1):
            #print(vectorOfWords[i])
            #print(type(vectorOfWords[i]), len(vectorOfWords[i]))


            if len(vectorOfWords[i])<3: continue #This is used to eliminate words like 'a' being added to our transcript list
            #
            # if self.lookUpByCompany[vectorOfWords[i]] != 0 :
            #     subList = self.helpGetSubVectorList(i, num, vectorOfWords)
            #     company[self.lookUpByCompany[vectorOfWords[i]]] = subList

            if self.lookUpBySymbol[vectorOfWords[i]] != 0\
                    or self.lookUpBySymbol[vectorOfWords[i].lower()] != 0\
                    or self.lookUpBySymbol[vectorOfWords[i].upper()] != 0:
                subList = self.helpGetSubVectorList(i, num, vectorOfWords)
                company[vectorOfWords[i]] = subList

        return company


    def helpGetSubVectorList(self, i, num, vectorOfWords):
        if i < num:
            lsLeft = vectorOfWords[0:i]
        else:
            lsLeft = vectorOfWords[i - num:i]
        if len(vectorOfWords) < i + num + 1:
            lsRight = vectorOfWords[i + 1:len(vectorOfWords)]
        else:
            lsRight = vectorOfWords[i + 1:num + 1]
        return lsLeft+lsRight
    #
    # def general(self, vectorOfWords):
    #     companyWordCount = defaultdict(int)
    #     companyWordIndex = defaultdict(int)
    #
    #     companyWordCount = defaultdict(int)
    #     companyWordIndex = defaultdict(int)
    #
    #     for word in vectorOfWords:
    #         if self.lookUpByCompany[word]!=0:
    #             companyWordCount[word]+=1
    #







if __name__ == "__main__":
    """4.4.20 Test for getting Crypt Data"""
    StockAssociation()


    """3.27.20 Test for Checking symbols added properly"""
    #TODO Not that GME not added, so I have to import more symbols
    # Also Not that Captilization may make a difference so take care of that.....
    """4.4.20 Test for Checking symbols added properly"""
    #TODO Huge problem, the crypto symbols interfer with Stock symbols
    # May need to create other data strucutre for crypto
    # Also intresting, there are GME crypto symbols assets associated with
    # GME as the underlying assest...... This is true for APPPLE and many other assests
    # Not sure what to do about this other than create seperate lookup tables for now
    print("GME", StockAssociation().lookUpBySymbol["GME"])

    print("AMD", StockAssociation().lookUpBySymbol["AMD"])

    print("APPL", StockAssociation().lookUpBySymbol["AAPL"])

    print("MSFT", StockAssociation().lookUpBySymbol["MSFT"])

    print("Nokia", StockAssociation().lookUpBySymbol["NOK"])


