import praw
from praw.models import MoreComments
from .wcdeneme import wordcloud_function
from textblob import TextBlob
import pandas as pd
from .utctodatetime import timeConverter
from .sentiment import getPolarity,getSubjectivity

def reddit_function(user,keyword, limit_value, sort):
    reddit = praw.Reddit(
        client_id='SQqqgzCGYZua-A',
        client_secret='HcI0XOLw7TDsq-wjAucvJ5jaQiF5Kg',
        user_agent='prawtutorial'
    )

    subreddit = reddit.subreddit(keyword)

    if sort == "hot":
        new_subreddit = subreddit.hot(limit=limit_value)
    elif sort == "top":
        new_subreddit = subreddit.top(limit=limit_value)
    else:
        new_subreddit = subreddit.new(limit=limit_value)

    result = []
    textforwc = []

    for i in new_subreddit:
        keys = ["user","post_id", "post", "score", "author", "subreddit","createdTime", "comment","subjectivity","polarity"]
        values = [user,i.id, i.title, i.score, i.author.name, i.subreddit.display_name,timeConverter(i.created_utc)]
        textforwc.append(i.title)
        submission = reddit.submission(id=i.id)
        comment_array = []
        subjectivity_array=[]
        polarity_array=[]

        analysis=TextBlob(i.title)
        subjectivity_array.append(analysis.sentiment.subjectivity)
        polarity_array.append(analysis.sentiment.polarity)

        try:
            for top_level_comment in submission.comments:
                if isinstance(top_level_comment, MoreComments):
                    continue
                comment_array.append(top_level_comment.body)
                textforwc.append(top_level_comment.body)
                analysis=TextBlob(top_level_comment.body)
                subjectivity_array.append(analysis.sentiment.subjectivity)
                polarity_array.append(analysis.sentiment.polarity)
                values.append(comment_array)
                values.append(subjectivity_array)
                values.append(polarity_array)

        except KeyError:
            continue
        
        result.append(dict(zip(keys, values)))
    print("array uzunlugu")
    print(len(textforwc))
    print(100*"#")
    df=pd.DataFrame(data=result)
    commentdf=pd.DataFrame(data=[item for item in textforwc],columns=['comments'])
    
    commentdf['Subjectivity']=commentdf['comments'].apply(getSubjectivity)
    commentdf['Polarity']=commentdf['comments'].apply(getPolarity)
    #print(df)
    print(commentdf)

    wordcloudtext = " ".join(textforwc)
    wcinstance = wordcloud_function(wordcloudtext)
    return df, wcinstance, commentdf
