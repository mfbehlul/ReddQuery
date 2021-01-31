import psycopg2
from datetime import date
import pandas as pd


def saveTheQuery(data, name):
    conn = psycopg2.connect(
        database="",
        user="",
        password="",
        host="",
        port=""
    )

    cur = conn.cursor()

    for item in data:
        cur.execute("INSERT INTO results_results(author,subreddit,comment,polarity,subjectivity,querydate,queryuser,sentiment)values(%s,%s,%s,%s,%s,%s,%s,%s)",
                    (item["author"], item["subreddit"], item["comment"], item["polarity"], item["subjectivity"], date.today(), name, item["sentiment"]))

    conn.commit()
    cur.close()
    conn.close()


def deleteTheQuery(querykeyword, queryuser, querydate):
    conn = psycopg2.connect(
        database="",
        user="",
        password="",
        host="",
        port=""
    )

    cur = conn.cursor()
   
    cur.execute("DELETE FROM results_results WHERE subreddit=%s AND queryuser=%s AND querydate=%s", (querykeyword,queryuser,querydate,))

    conn.commit()
    conn.close()

def fetchTheQuery():

    conn = psycopg2.connect(
        database="",
        user="",
        password="",
        host="",
        port=""
    )

    cur = conn.cursor()

    cur.execute("select author, subreddit, comment, polarity, subjectivity, querydate, queryuser, sentiment from results_results")
    headers=["author","subreddit","comment", "polarity","subjectivity","querydate","queryuser","sentiment"]
    rows=cur.fetchall()
    df=pd.DataFrame(rows,columns=headers)
    conn.commit()
    cur.close()
    conn.close()
    return df