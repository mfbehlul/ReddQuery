import praw
from praw.models import MoreComments
from .wcdeneme import wordcloud_function


def reddit_function(keyword, limit_value, sort):
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
        keys = ["post_id", "post", "score", "author", "subreddit", "comment"]
        values = [i.id, i.title, i.score, i.author.name, i.subreddit.display_name]
        textforwc.append(i.title)
        print(values)
        submission = reddit.submission(id=i.id)
        comment_array = []

        try:
            for top_level_comment in submission.comments:
                if isinstance(top_level_comment, MoreComments):
                    continue
                comment_array.append(top_level_comment.body)
                textforwc.append(top_level_comment.body)
                values.append(comment_array)

        except KeyError:
            continue
        
        result.append(dict(zip(keys, values)))
    print("array uzunlugu")
    print(len(textforwc))
    print(100*"#")
    wordcloudtext = " ".join(textforwc)
    wcinstance = wordcloud_function(wordcloudtext)
    return result, wcinstance
