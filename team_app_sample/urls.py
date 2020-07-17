"""team_app_sample URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from team import views as team_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', team_views.index, name='index'),
    path('send', team_views.send, name='send'),
    path('announce', team_views.announce, name='announce'),
    path('api/join', team_views.join, name='api_join'),
    path('api/team_help', team_views.team_help, name='api_team_help'), #HIEU AND HAI
    path('api/recipe', team_views.recipe, name='api_get_Recipe'),
]
