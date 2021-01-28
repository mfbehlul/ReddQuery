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




# Create your views here.

global_datakeyword = {}
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

    if (key != "") & (savevalue == ""):

        datakeyword, wcinstance, commentdata = reddit_function(user=request.user,
                                                               keyword=key, limit_value=limit, sort=sortby)

        # print(datakeyword)
        json_records = datakeyword.reset_index().to_json(orient='records')
        dataJson = []
        dataJson = json.loads(json_records)
        global_wcinstance = wcinstance
        global_datakeyword = dataJson
        context = {"data": dataJson,
                   "wcimage": wcinstance}

    name=str(request.user)
    if (savevalue != "") & (key == ""):

        saveTheQuery(global_datakeyword,name)
        
    return render(request, 'homepage.html', context)


def table_view(request):
    context = {"data": global_datakeyword}

    return render(request, 'tables.html', context)


def wordcloud_view(request):
    context = {"wcimage": global_wcinstance}

    return render(request, 'wordcloud.html', context)
