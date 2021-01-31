from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.views import login
from .redditapi import reddit_function
from results.models import Results
import psycopg2
import praw
from .wc import wordcloud_function
from .save import saveTheQuery
import json
from results.models import Results
import pandas as pd
import re
from .deletequery import deleteTheQuery
from .sentiment import plotTheSentiment

# Create your views here.

global_datakeyword = []
global_wcinstance = ""
global_sentimentinstance = ""


@login_required(login_url='login')
def home_view(request):
    global global_datakeyword
    global global_wcinstance
    global global_sentimentinstance

    text = request.GET
    
    key = text.get("keyword", "")
    limit = int(text.get("limit", 10))
    sortby = str(text.get("sortby", ""))
    isSearch="False"

    if key == "":
        global_sentimentinstance = ""
        global_wcinstance = ""
        global_datakeyword = [{'index': 1, 'Comment': '',
                               'Subjectivity': 0.6666666667, 'Polarity': -0.5, 'Querydate': '2021-01-07', 'Subreddit': 'litecoin', 'Author': 'Blitzpocket'}]

    if key != "":
        wcinstance, commentdata = reddit_function(user=request.user,
                                                  keyword=key, limit_value=limit, sort=sortby)

        json_records = commentdata.reset_index().to_json(orient='records')
        dataJson = []
        dataJson = json.loads(json_records)
        global_datakeyword = dataJson
        global_wcinstance = wcinstance
        #print(type(commentdata))
        global_sentimentinstance = plotTheSentiment(commentdata)
        isSearch="True"
        

    context = {"isSearch":isSearch}
    return render(request, 'homepage.html', context)


def table_view(request):
    text=request.GET
    savevalue = text.get("savebutton", "")
    name = str(request.user)
    
    tablesaved="False"
    if savevalue != "":
        saveTheQuery(global_datakeyword, name)
       
        tablesaved="True"
        

    context = {"data": global_datakeyword,"isSaved":tablesaved}

    return render(request, 'tables.html', context)


def wordcloud_view(request):
    context = {"wcimage": global_wcinstance}

    return render(request, 'wordcloud.html', context)


def sentiment_view(request):

    context = {"sentimentimage": global_sentimentinstance}
    return render(request, 'sentiment.html', context)


def savedquery_view(request):
    text = request.GET
    global global_datakeyword
    global global_wcinstance
    global global_sentimentinstance
    global_sentimentinstance = ""
    global_wcinstance = ""
    global_datakeyword = [{'index': 0, 'Comment': '',
                               'Subjectivity': 0, 'Polarity':0 , 'Querydate': '2021-01-07', 'Subreddit': 'litecoin', 'Author': 'Blitzpocket'}]

    issaved="False"
    conn = psycopg2.connect(
        database="da4973spbbo8pi",
        user="fyffloodpxarwp",
        password="552eb5c1db0ddc25a9ab1bb8dbc46b822334782e1cd8a55b0f50270749f0caef",
        host="ec2-54-235-158-17.compute-1.amazonaws.com",
        port="5432"
    )

    cur = conn.cursor()

    cur.execute("select author, subreddit, comment, polarity, subjectivity, querydate, queryuser, sentiment from results_results")
    headers=["author","subreddit","comment", "polarity","subjectivity","querydate","queryuser","sentiment"]
    rows=cur.fetchall()
    df=pd.DataFrame(rows,columns=headers)
    conn.commit()
    cur.close()
    conn.close()

    """results = list(Results.objects.all())

    database_results = []
    for i in results:
        keys = ['author', 'subreddit', 'comment', 'polarity',
                'subjectivity', 'querydate', 'queryuser', 'sentiment']
        values = [i.author, i.subreddit, i.comment, i.polarity,
                  i.subjectivity, i.querydate, i.queryuser, i.sentiment]
        database_results.append(dict(zip(keys, values)))

    df = pd.DataFrame(database_results, columns=[
        'author', 'subreddit', 'comment', 'polarity', 'subjectivity', 'querydate', 'queryuser', 'sentiment'])"""

    df = df[df["queryuser"] == str(request.user)]

    dates = list(df["querydate"])
    subreddits = list(df["subreddit"])
    dates_and_keywords = list(set(zip(dates, subreddits)))
    selected_query = text.get("query", "")

    if selected_query != "":
        splitted_value = re.search("('(.*)')", selected_query)

        splitted_value_list = splitted_value.group(1).split(',')

        selected_keyword = re.search("'(.*)'", splitted_value_list[1])
        selected_keyword = selected_keyword.group(1)

        selected_date = re.search("'(.*)'", splitted_value_list[0])
        selected_date = selected_date.group(1)

        df = df[df["subreddit"] == selected_keyword]
        df = df[df["querydate"] == selected_date]

        json_records = df.reset_index().to_json(orient='records')
        final_result = []
        final_result = json.loads(json_records)

        global_datakeyword = final_result

        comment_list = df["comment"].to_list()
        wordcloudtext = " ".join(comment_list)
        wcinstance = wordcloud_function(wordcloudtext)

        global_wcinstance = wcinstance
        # print(df)
        # print(df["polarity"].value_counts())
        print(type(df))
        global_sentimentinstance = plotTheSentiment(df)
        issaved="True"

    context = {"searchword": dates_and_keywords,"isSearch":issaved}

    return render(request, 'savedquery.html', context)


def deletequery_view(request):
    text = request.GET
    global global_datakeyword
    global global_wcinstance
    global global_sentimentinstance
    global_sentimentinstance = ""
    global_wcinstance = ""
    global_datakeyword = [{'index': 0, 'Comment': '',
                               'Subjectivity': 0, 'Polarity':0 , 'Querydate': '2021-01-07', 'Subreddit': 'litecoin', 'Author': 'Blitzpocket'}]
    isdeleted="False"
    conn = psycopg2.connect(
        database="da4973spbbo8pi",
        user="fyffloodpxarwp",
        password="552eb5c1db0ddc25a9ab1bb8dbc46b822334782e1cd8a55b0f50270749f0caef",
        host="ec2-54-235-158-17.compute-1.amazonaws.com",
        port="5432"
    )

    cur = conn.cursor()

    cur.execute("select author, subreddit, comment, polarity, subjectivity, querydate, queryuser, sentiment from results_results")
    headers=["author","subreddit","comment", "polarity","subjectivity","querydate","queryuser","sentiment"]
    rows=cur.fetchall()
    df=pd.DataFrame(rows,columns=headers)
    conn.commit()
    cur.close()
    conn.close()

    """
    results = list(Results.objects.all())

    database_results = []
    for i in results:
        keys = ['author', 'subreddit', 'comment', 'polarity',
                'subjectivity', 'querydate', 'queryuser', 'sentiment']
        values = [i.author, i.subreddit, i.comment, i.polarity,
                  i.subjectivity, i.querydate, i.queryuser, i.sentiment]
        database_results.append(dict(zip(keys, values)))

    df = pd.DataFrame(database_results, columns=[
        'author', 'subreddit', 'comment', 'polarity', 'subjectivity', 'querydate', 'queryuser', 'sentiment'])"""

    df = df[df["queryuser"] == str(request.user)]

    dates = list(df["querydate"])
    subreddits = list(df["subreddit"])
    dates_and_keywords = list(set(zip(dates, subreddits)))
    selected_query = text.get("query", "")

    if selected_query != "":
        splitted_value = re.search("('(.*)')", selected_query)

        splitted_value_list = splitted_value.group(1).split(',')

        selected_keyword = re.search("'(.*)'", splitted_value_list[1])
        selected_keyword = selected_keyword.group(1)

        selected_date = re.search("'(.*)'", splitted_value_list[0])
        selected_date = selected_date.group(1)
        deleteTheQuery(selected_keyword, str(request.user), selected_date)
        isdeleted="True"

    context = {"searchword": dates_and_keywords,"isSearch":isdeleted}
    return render(request, 'deletequery.html', context)
