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
global_sentimentinstance=""


@login_required(login_url='login')
def home_view(request):
    global global_datakeyword
    global global_wcinstance
    global global_sentimentinstance

    text = request.GET
    context = {}
    key = text.get("keyword", "")
    limit = int(text.get("limit", 10))
    sortby = str(text.get("sortby", ""))
    savevalue = text.get("savebutton", "")

    if savevalue == "":
        global_sentimentinstance=""
        global_wcinstance = ""
        global_datakeyword = [{'index': 1, 'Comment': '',
                               'Subjectivity': 0.6666666667, 'Polarity': -0.5, 'Querydate': '2021-01-07', 'Subreddit': 'litecoin', 'Author': 'Blitzpocket'}]

    if (key != "") & (savevalue == ""):
        wcinstance, commentdata = reddit_function(user=request.user,
                                                  keyword=key, limit_value=limit, sort=sortby)

        json_records = commentdata.reset_index().to_json(orient='records')
        dataJson = []
        dataJson = json.loads(json_records)
        global_datakeyword = dataJson
        global_wcinstance = wcinstance
        global_sentimentinstance=plotTheSentiment(commentdata)
        context = {}

    name = str(request.user)
    if (savevalue != "") & (key == ""):

        saveTheQuery(global_datakeyword, name)

    return render(request, 'homepage.html', context)


def table_view(request):
    context = {"data": global_datakeyword}

    return render(request, 'tables.html', context)


def wordcloud_view(request):
    context = {"wcimage": global_wcinstance}

    return render(request, 'wordcloud.html', context)

def sentiment_view(request):
    
    context={"sentimentimage":global_sentimentinstance}
    return render(request,'sentiment.html',context)

def savedquery_view(request):
    text = request.GET
    global global_datakeyword
    global global_wcinstance
    global global_sentimentinstance

    results = list(Results.objects.all())

    database_results = []
    for i in results:
        keys = ['author', 'subreddit', 'comment', 'polarity',
                'subjectivity', 'querydate', 'queryuser', 'sentiment']
        values = [i.author, i.subreddit, i.comment, i.polarity,
                  i.subjectivity, i.querydate, i.queryuser, i.sentiment]
        database_results.append(dict(zip(keys, values)))

    df = pd.DataFrame(database_results, columns=[
        'author', 'subreddit', 'comment', 'polarity', 'subjectivity', 'querydate', 'queryuser', 'sentiment'])

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

        comment_list=df["comment"].to_list()
        wordcloudtext = " ".join(comment_list)
        wcinstance = wordcloud_function(wordcloudtext)
        global_wcinstance = wcinstance
        global_sentimentinstance=plotTheSentiment(df)

    context = {"searchword": dates_and_keywords}

    return render(request, 'savedquery.html', context)


def deletequery_view(request):
    text=request.GET
    results = list(Results.objects.all())

    database_results = []
    for i in results:
        keys = ['author', 'subreddit', 'comment', 'polarity',
                'subjectivity', 'querydate', 'queryuser', 'sentiment']
        values = [i.author, i.subreddit, i.comment, i.polarity,
                  i.subjectivity, i.querydate, i.queryuser, i.sentiment]
        database_results.append(dict(zip(keys, values)))

    df = pd.DataFrame(database_results, columns=[
        'author', 'subreddit', 'comment', 'polarity', 'subjectivity', 'querydate', 'queryuser', 'sentiment'])

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
        deleteTheQuery(selected_keyword,str(request.user),selected_date)

    context = {"searchword": dates_and_keywords}
    return render (request,'deletequery.html',context)