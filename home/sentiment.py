from textblob import TextBlob
import pandas as pd
import numpy as np
import re

def cleanText(text):
    text=re.sub(r'https?:\/\/\S+','',text)
    text=re.sub(r'deleted','',text)
    return text

def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
    return TextBlob(text).sentiment.polarity
