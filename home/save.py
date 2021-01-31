import psycopg2
import praw
from praw.models import MoreComments
from datetime import date


def saveTheQuery(data, name):
    conn = psycopg2.connect(
        database="da4973spbbo8pi",
        user="fyffloodpxarwp",
        password="552eb5c1db0ddc25a9ab1bb8dbc46b822334782e1cd8a55b0f50270749f0caef",
        host="ec2-54-235-158-17.compute-1.amazonaws.com",
        port="5432"
    )

    cur = conn.cursor()

    for item in data:
        cur.execute("INSERT INTO results_results(author,subreddit,comment,polarity,subjectivity,querydate,queryuser,sentiment)values(%s,%s,%s,%s,%s,%s,%s,%s)",
                    (item["author"], item["subreddit"], item["comment"], item["polarity"], item["subjectivity"], date.today(), name, item["sentiment"]))

    conn.commit()
    cur.close()
    conn.close()
