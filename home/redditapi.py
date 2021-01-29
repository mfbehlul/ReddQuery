import praw
from praw.models import MoreComments
from .wcdeneme import wordcloud_function
from textblob import TextBlob
import pandas as pd
from .utctodatetime import timeConverter
from .sentiment import getPolarity, getSubjectivity
from .sentiment import cleanText


def reddit_function(user, keyword, limit_value, sort):
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
    comment_array = []
    subjectivity_array = []
    polarity_array = []
    createdtime_array = []
    subreddit_array = []
    author_array = []

    for i in new_subreddit:
        keys = ["user", "postid", "title", "score", "author",
                "subreddit", "querydate", "comment", "subjectivity", "polarity"]
        values = [user, i.id, i.title, i.score, i.author.name,
                  i.subreddit.display_name, timeConverter(i.created_utc)]
        # textforwc.append(i.title)
        submission = reddit.submission(id=i.id)
        

        #analysis = TextBlob(i.title)
        # subjectivity_array.append(analysis.sentiment.subjectivity)
        # polarity_array.append(analysis.sentiment.polarity)

        try:
            for top_level_comment in submission.comments:
                if isinstance(top_level_comment, MoreComments):
                    continue

                cleaned_comment = cleanText(top_level_comment.body)
                if (len(cleaned_comment) < 7) or (top_level_comment.author==None):
                    continue
                comment_array.append(cleaned_comment)
                textforwc.append(cleaned_comment)
                analysis = TextBlob(cleaned_comment)
                subjectivity_array.append(analysis.sentiment.subjectivity)
                polarity_array.append(analysis.sentiment.polarity)
                createdtime_array.append(
                    timeConverter(top_level_comment.created_utc))
                subreddit_array.append(top_level_comment.subreddit.display_name)
                author_array.append(top_level_comment.author.name)

              

                values.append(comment_array)
                values.append(subjectivity_array)
                values.append(polarity_array)

        except KeyError:
            continue

        result.append(dict(zip(keys, values)))
    print("array uzunlugu")
    print(len(textforwc))
    print(100*"#")
  

    commentdf = pd.DataFrame(
        data=[item for item in textforwc], columns=['comment'])

    commentdf['subjectivity'] = commentdf['comment'].apply(getSubjectivity)
    commentdf['polarity'] = commentdf['comment'].apply(getPolarity)
    commentdf['querydate'] = createdtime_array
    commentdf['subreddit'] = subreddit_array
    commentdf['author'] = author_array

    wordcloudtext = " ".join(textforwc)
    wcinstance = wordcloud_function(wordcloudtext)
    return result, wcinstance, commentdf
