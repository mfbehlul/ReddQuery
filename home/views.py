from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.views import login
from .redditapi import reddit_function
from results.models import Results
import psycopg2
import praw
from .wcdeneme import wordcloud_function
from .save import saveTheQuery


# Create your views here.

global_datakeyword={}

@login_required(login_url='login')
def home_view(request):
    global global_datakeyword
    text = request.GET
    context = {}
    key = text.get("keyword", "")
    limit = int(text.get("limit", 10))
    sortby = str(text.get("sortby", ""))
    savevalue=text.get("savebutton","")

    if (key != "")&(savevalue==""):

        datakeyword,wcinstance = reddit_function(
            keyword=key, limit_value=limit, sort=sortby)

        global_datakeyword=datakeyword
        context = {"data": datakeyword,
                   "table": "visible", "wcimage": wcinstance}

    if (savevalue !="")&(key==""):
        saveTheQuery(global_datakeyword)
        
    return render(request, 'homepage.html', context)

