from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
import io
import urllib
import base64



def wordcloud_function(text):
    string2=""
    image642=""
    stopwords = {'wtf','fucking','fuck','http','https','one','yet','Redditor','name','display_name','subreddit','too', 'hers', 'how', "what's", 'on', 'him', "i'd", "they'll", 'myself', "shouldn't", 'about', 'http', 'hence', 'can', 'ever', "she's", 'as', "couldn't", 'themselves', 'your', 'we', 'are', 'some', "how's", "aren't", 'any', "he's", 'being', 'its', "you've", "they're", 'ours', "where's", 'other', 'of', "it's", "there's", 'out', 'they', 'her', 'be', "here's", "let's", 'until', 'or', 'where', "wouldn't", "when's", "we'd", "he'd", "i've", 'yourself', "don't", 'had', 'herself', 'does', "she'd", "mustn't", 'doing', 'from', "hasn't", "doesn't", 'what', 'yours', "we're", "i'm", 'few', 'www', 'while', 'under', 'in', 'the', 'before', "can't", "wasn't", 'ourselves', "they've", 'through', 'since', "won't", 'which', 'if', 'am', 'and', 'who', 'into', "we've", 'else', 'has', 'so', 'most', 'very', 'but', 'with',
                 'both', 'cannot', 'otherwise', 'here', 'i', 'down', 'nor', 'could', "you'd", 'itself', 'not', 'than', 'off', 'like', "you'll", "we'll", "he'll", 'com', 'having', 'did', 'also', 'r', 'there', "why's", 'should', 'all', 'yourselves', 'my', 'therefore', 'those', 'just', "i'll", 'such', 'because', "shan't", 'by', 'were', 'each', 'would', "that's", 'this', 'it', 'me', 'then', 'once', 'only', 'again', 'our', 'up', 'do', 'was', 'been', 'no', 'ought', 'over', 'get', 'a', "weren't", 'own', 'same', "hadn't", 'you', 'an', "isn't", 'further', 'he', 'theirs', 'after', 'have', 'k', "didn't", 'shall', 'at', 'during', 'below', 'when', 'them', 'to', 'however', 'that', 'is', 'between', "haven't", 'for', 'against', 'why', 'she', 'these', 'himself', 'more', 'their', 'his', "you're", 'whom', "they'd", 'above', "who's", "she'll"}

   
    cloud_text = WordCloud(background_color="white", max_font_size=200, max_words=120,
                           stopwords=stopwords, height=1000, width=1500).generate(text)
    plt.imshow(cloud_text, interpolation="bilinear")
    plt.axis("off")
    

    image2=io.BytesIO()
    plt.savefig(image2,format='png')
    image2.seek(0)
    string2=base64.b64encode(image2.read())
    image642='data:image2/png;base64,'+urllib.parse.quote(string2)
    return image642





