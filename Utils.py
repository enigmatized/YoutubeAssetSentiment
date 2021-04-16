import re

class Utils:

    @staticmethod
    def vectorOfWords(string):
        wordList = re.sub("[^\w]", " ", string).split()
        return wordList

    @staticmethod
    def vectorOfWordsToString(ls):
        result =""
        for word in ls:
            result = result +" "+word
        return result

