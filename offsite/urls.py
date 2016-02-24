"""ovenbird URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views import ShowOvenbird, UpdateObject, CreateObject, ShowObject, DeleteObject
from .views import CreateOvenbird, UpdateOvenbird, AddFile
from . import views
#from offsite.views import AboutView

urlpatterns = [
    url(r'^$', views.MainPage, name="index"),
    url(r'^myprofile/$', UpdateOvenbird.as_view(), name='myprofile'),
    url(r'^ShowOvenbird/(?P<ovenbird_id>\d+)/$', ShowOvenbird.as_view(), name="showovenbird"),
    url(r'^CreateOvenbird/$', CreateOvenbird.as_view(), name="createovenbird"),
    url(r'^CreateObject/$', CreateObject.as_view(), name='createobject'),
    url(r'^CreateArticle/$', views.CreateArticle, name='createarticle'),
    url(r'^ShowObject/(?P<pk>\d+)/$', ShowObject.as_view(), name='showobject'),
    url(r'^ShowArticle/(?P<article_id>\d+)/$', views.ShowArticle, name='showarticle'),
    url(r'^UpdateObject/(?P<pk>\d+)/$', UpdateObject.as_view(), name='updateobject'),
    url(r'^DeleteObject/(?P<pk>\d+)/$', DeleteObject.as_view(), name='deleteobject'),
    url(r'^AddFile/(?P<pk>\d+)/$', AddFile.as_view(), name='addfile')
]