import psycopg2
import praw
from praw.models import MoreComments

def saveTheQuery(data):
    conn = psycopg2.connect(
        database="da4973spbbo8pi",
        user="fyffloodpxarwp",
        password="552eb5c1db0ddc25a9ab1bb8dbc46b822334782e1cd8a55b0f50270749f0caef",
        host="ec2-54-235-158-17.compute-1.amazonaws.com",
        port="5432"
    )
    
    reddit = praw.Reddit(
        client_id='SQqqgzCGYZua-A',
        client_secret='HcI0XOLw7TDsq-wjAucvJ5jaQiF5Kg',
        user_agent='prawtutorial'
    )
    cur = conn.cursor()

    for item in data:

        submission = reddit.submission(id=item["post_id"])

        try:
            for top_level_comment in submission.comments:
                if isinstance(top_level_comment, MoreComments):
                    continue

                cur.execute("INSERT INTO results_results(title,postid,score,author,subreddit,comment)values(%s,%s,%s,%s,%s,%s)",
                            (item["post"], item["post_id"], item["score"], item["author"], item["subreddit"], top_level_comment.body))

        except KeyError:
            continue

    conn.commit()

    conn.close()
