import praw
from praw.models import MoreComments
from .wc import wordcloud_function
from textblob import TextBlob
import pandas as pd
from .utctodatetime import timeConverter
from .sentiment import cleanText
from .sentiment import getPolarity,getSubjectivity,getPolarityResult


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

    textforwc = []
    createdtime_array = []
    subreddit_array = []
    author_array = []

    for i in new_subreddit:
        submission = reddit.submission(id=i.id)

        try:
            for top_level_comment in submission.comments:
                if isinstance(top_level_comment, MoreComments):
                    continue

                cleaned_comment = cleanText(top_level_comment.body)
                if (len(cleaned_comment) < 7) or (top_level_comment.author == None):
                    continue

                textforwc.append(cleaned_comment)
                createdtime_array.append(
                    timeConverter(top_level_comment.created_utc))

                subreddit_array.append(
                    top_level_comment.subreddit.display_name)
                author_array.append(top_level_comment.author.name)

        except KeyError:
            continue

    commentdf = pd.DataFrame(
        data=[item for item in textforwc], columns=['comment'])

    commentdf['subjectivity'] = commentdf['comment'].apply(getSubjectivity)
    commentdf['polarity'] = commentdf['comment'].apply(getPolarity)
    commentdf['sentiment']=commentdf['polarity'].apply(getPolarityResult)
    commentdf['querydate'] = createdtime_array
    commentdf['subreddit'] = subreddit_array
    commentdf['author'] = author_array

    wordcloudtext = " ".join(textforwc)
    wcinstance = wordcloud_function(wordcloudtext)
    return wcinstance, commentdf
