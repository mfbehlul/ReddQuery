from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.views import login
from .redditapi import reddit_function
from results.models import Results
import psycopg2
import praw
from .wcdeneme import wordcloud_function
from .save import saveTheQuery
import json
from results.models import Results


# Create your views here.

global_datakeyword = []
global_wcinstance = ""


@login_required(login_url='login')
def home_view(request):
    global global_datakeyword
    global global_wcinstance

   
    text = request.GET
    context = {}
    key = text.get("keyword", "")
    limit = int(text.get("limit", 10))
    sortby = str(text.get("sortby", ""))
    savevalue = text.get("savebutton", "")
    print("home view a girdi")
    if savevalue=="":
         global_datakeyword = [{'index': 1, 'Comment': '',
                           'Subjectivity': 0.6666666667, 'Polarity': -0.5, 'Querydate': '2021-01-07', 'Subreddit': 'litecoin', 'Author': 'Blitzpocket'}]

    if (key != "") & (savevalue == ""):
        print("homeview ife girdi")
        datakeyword, wcinstance, commentdata = reddit_function(user=request.user,
                                                               keyword=key, limit_value=limit, sort=sortby)

        json_records = commentdata.reset_index().to_json(orient='records')
        dataJson = []
        dataJson = json.loads(json_records)
        global_wcinstance = wcinstance

        global_datakeyword = dataJson
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


def savedquery_view(request):
    global global_datakeyword
    results = list(Results.objects.all())
    global_datakeyword = results
    name_list=[]
    for name in results:
        name_list.append(name.queryuser)
    name_list=list(dict.fromkeys(name_list))
    print(name_list)
    context = {}
    

    return render(request, 'savedquery.html', context)
