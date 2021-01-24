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


@login_required(login_url='login')
def home_view(request):
    global global_datakeyword
    text = request.GET
    context = {}
    key = text.get("keyword", "")
    limit = int(text.get("limit", 10))
    sortby = str(text.get("sortby", ""))
    savevalue = text.get("savebutton", "")

    if (key != "") & (savevalue == ""):

        datakeyword, wcinstance, commentdata = reddit_function(user=request.user,
                                                  keyword=key, limit_value=limit, sort=sortby)

        json_records = datakeyword.reset_index().to_json(orient='records')
        dataJson = []
        dataJson = json.loads(json_records)
        
        global_datakeyword = dataJson
        context = {"data": dataJson,
                   "table": "visible", "wcimage": wcinstance}

    if (savevalue != "") & (key == ""):
        saveTheQuery(global_datakeyword)

    return render(request, 'homepage.html', context)
