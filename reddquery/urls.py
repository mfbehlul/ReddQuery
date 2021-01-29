"""reddquery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home.views import home_view
from home.views import table_view
from home.views import wordcloud_view
from home.views import savedquery_view
from accounts.views import login_view,register_view
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view,name="home"),
    path('login/', login_view, name="login"),
    path('logout/', login_view, name="logout"),
    path('register/', register_view, name="register"),
    path('tables/', table_view, name="tables"),
    path('wordcloud/', wordcloud_view, name="wordcloud"),
    path('savedquery/', savedquery_view, name="savedquery"),
]
