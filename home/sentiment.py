from textblob import TextBlob
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import io
import urllib
import base64

def cleanText(text):
    text=re.sub(r'https?:\/\/\S+','',text)
    text=re.sub(r'deleted','',text)
    return text

def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
    return TextBlob(text).sentiment.polarity

def getPolarityResult(text):
    if text>=0.7:
        return 'Very Positive'
    elif (text<0.7) and (text>=0.3):
        return 'Positive'
    elif (text<0.3) and (text>=-0.3):
        return 'Neutral'
    elif (text<-0.3) and (text>=-0.7):
        return 'Negative'
    elif (text<-0.7) and (text>=-1):
        return 'Very Negative'

def plotTheSentiment(df):
    plt.figure(figsize=(8,6))
    for i in range(0,df.shape[0]):
        plt.scatter(df["polarity"][i],df["subjectivity"][i], color="Blue")

    plt.title("Sentiment Analysis")
    plt.xlabel("Polarity")
    plt.ylabel("Subjectivity")
    plt.show()
    
    image=io.BytesIO()
    plt.savefig(image,format='png')
    image.seek(0)
    string=base64.b64encode(image.read())
    image64='data:image/png;base64,'+urllib.parse.quote(string)
    return image64