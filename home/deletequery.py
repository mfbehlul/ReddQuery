import psycopg2


def deleteTheQuery(querykeyword, queryuser, querydate):
    conn = psycopg2.connect(
        database="da4973spbbo8pi",
        user="fyffloodpxarwp",
        password="552eb5c1db0ddc25a9ab1bb8dbc46b822334782e1cd8a55b0f50270749f0caef",
        host="ec2-54-235-158-17.compute-1.amazonaws.com",
        port="5432"
    )

    cur = conn.cursor()
   
    cur.execute("DELETE FROM results_results WHERE subreddit=%s AND queryuser=%s AND querydate=%s", (querykeyword,queryuser,querydate,))

    conn.commit()
    conn.close()
