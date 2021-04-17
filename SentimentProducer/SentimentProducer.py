import pandas as pd
import re
from textblob import TextBlob

class SentimentProducer:
    def __init__(self):
        pass

    def produceSentiment(self):
        pass

    @staticmethod
    def getSubjectivity(text):
        return TextBlob(text).sentiment.subjectivity

    @staticmethod
    def getPolarity(text):
        return TextBlob(text).sentiment.polarity

    @staticmethod
    def getAnalysis(score):
        if score < 0:
            return 'Neg'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Pos'
