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

        try:
            for top_level_comment, polarity_value, subjectivity_value in zip(item["comment"], item["polarity"], item["subjectivity"]):

                cur.execute("INSERT INTO results_results(title,postid,score,author,subreddit,comment,polarity,subjectivity,querydate,queryuser)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            (item["post"], item["post_id"], item["score"], item["author"], item["subreddit"], top_level_comment, polarity_value, subjectivity_value, date.today(),name ))

        except KeyError:
            continue

    conn.commit()
    conn.close()
