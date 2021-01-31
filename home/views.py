from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.views import login
from .redditapi import reddit_function
from results.models import Results
import psycopg2
import praw
from .wc import wordcloud_function
from .database import saveTheQuery, deleteTheQuery, fetchTheQuery
import json
from results.models import Results
import pandas as pd
import re
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
    isSearch = "False"

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
        global_sentimentinstance = plotTheSentiment(commentdata)
        isSearch = "True"

    context = {"isSearch": isSearch}
    return render(request, 'homepage.html', context)


def table_view(request):
    text = request.GET
    savevalue = text.get("savebutton", "")
    name = str(request.user)

    tablesaved = "False"
    if savevalue != "":
        saveTheQuery(global_datakeyword, name)

        tablesaved = "True"

    context = {"data": global_datakeyword, "isSaved": tablesaved}

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
                           'Subjectivity': 0, 'Polarity': 0, 'Querydate': '2021-01-07', 'Subreddit': 'litecoin', 'Author': 'Blitzpocket'}]

    issaved = "False"
    df=fetchTheQuery()
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
        global_sentimentinstance = plotTheSentiment(df)
        issaved = "True"

    context = {"searchword": dates_and_keywords, "isSearch": issaved}

    return render(request, 'savedquery.html', context)


def deletequery_view(request):
    text = request.GET
    global global_datakeyword
    global global_wcinstance
    global global_sentimentinstance
    global_sentimentinstance = ""
    global_wcinstance = ""
    global_datakeyword = [{'index': 0, 'Comment': '',
                           'Subjectivity': 0, 'Polarity': 0, 'Querydate': '2021-01-07', 'Subreddit': 'litecoin', 'Author': 'Blitzpocket'}]
    isdeleted = "False"

    df = fetchTheQuery()
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
        isdeleted = "True"

    context = {"searchword": dates_and_keywords, "isSearch": isdeleted}
    return render(request, 'deletequery.html', context)
