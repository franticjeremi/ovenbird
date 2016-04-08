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
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.MainPage, name="index"),
    url(r'^Ovenbird/', include([
        url(r'^Show/(?P<ovenbird_id>\d+)/$', views.ShowOvenbird.as_view(), name="showovenbird"),
        url(r'^Create/$', views.CreateOvenbird.as_view(), name="createovenbird"),
        url(r'^MyProfile/$', views.UpdateOvenbird.as_view(), name='myprofile'),
    ])),
    #url(r'^myprofile/$', views.UpdateOvenbird.as_view(), name='myprofile'),
    #url(r'^ShowOvenbird/(?P<ovenbird_id>\d+)/$', views.ShowOvenbird.as_view(), name="showovenbird"),
    #url(r'^CreateOvenbird/$', views.CreateOvenbird.as_view(), name="createovenbird"),
    url(r'^Object/', include([
        url(r'^Create/$', views.CreateObject.as_view(), name='createobject'),
        url(r'^Show/(?P<pk>\d+)/$', views.ShowObject.as_view(), name='showobject'),
        url(r'^Update/(?P<pk>\d+)/$', views.UpdateObject.as_view(), name='updateobject'),
        url(r'^Delete/(?P<pk>\d+)/$', views.DeleteObject.as_view(), name='deleteobject'),
    ])),
    #url(r'^CreateObject/$', views.CreateObject.as_view(), name='createobject'),
    url(r'^CreateArticle/$', views.CreateArticle, name='createarticle'),
    #url(r'^ShowObject/(?P<pk>\d+)/$', views.ShowObject.as_view(), name='showobject'),
    url(r'^ShowArticle/(?P<article_id>\d+)/$', views.ShowArticle, name='showarticle'),
    #url(r'^UpdateObject/(?P<pk>\d+)/$', views.UpdateObject.as_view(), name='updateobject'),
    #url(r'^DeleteObject/(?P<pk>\d+)/$', views.DeleteObject.as_view(), name='deleteobject'),
    url(r'^File/', include([
        url(r'^Add/$', views.AddFile.as_view(), name='addfile'),
        url(r'^Show/$', views.ShowFile.as_view(), name='showfile'),
        url(r'^Delete/(?P<pk>\d+)/$', views.DeleteFile.as_view(), name='deletefile'),
        url(r'^ShowAll/(?P<object_id>\d+)$', views.ShowAllFile.as_view(), name='showallfile'),
        url(r'^JoinObject/(?P<pk>\d+)/(?P<object_id>\d+)/$', views.JoinObject.as_view(), name='joinobject'),
        url(r'^UnjoinObject/(?P<pk>\d+)/(?P<object_id>\d+)/$', views.UnjoinObject.as_view(), name='unjoinobject'),
        url(r'^GetList/(?P<object_id>\d+)/(?P<not_object_id>\d+)$', views.GetListFiles.as_view(), name='getlistfiles'),
    ])),
    #url(r'^AddFile/$', views.AddFile.as_view(), name='addfile'),
    #url(r'^ShowFile/$', views.ShowFile.as_view(), name='showfile'),
    #url(r'^DeleteFile/(?P<pk>\d+)/$', views.DeleteFile.as_view(), name='deletefile'),
    url(r'^GetListObjects/$', views.GetListObjects.as_view(), name='getlistobjects'),
    url(r'^GetListJoinedObjects/(?P<photo_id>\d+)/$', views.GetListJoinedObjects.as_view(), name='getlistjoinedobjects'),
    #url(r'^JoinObject/(?P<pk>\d+)/(?P<object_id>\d+)/$', views.JoinObject.as_view(), name='joinobject'),
    #url(r'^UnjoinObject/(?P<pk>\d+)/(?P<object_id>\d+)/$', views.UnjoinObject.as_view(), name='unjoinobject'),
    url(r'^MakeTitlePhoto/(?P<pk>\d+)/(?P<object_id>\d+)/$', views.MakeTitlePhoto.as_view(), name='maketitlephoto'),
    url(r'^SetOvenbirdPhoto/(?P<pk>\d+)/$', views.SetOvenbirdPhoto.as_view(), name='setovenbirdphoto'),
    url(r'^Adser/Show/$', views.ShowAdser.as_view(), name='showadser'),
    url(r'^Ads/', include([
        url(r'^Create/$', views.CreateAds.as_view(), name='createads'),
        url(r'^Update/(?P<pk>\d+)$', views.UpdateAds.as_view(), name='updateads'),
        url(r'^Delete/(?P<pk>\d+)$', views.DeleteAds.as_view(), name='deleteads'),
    ])),
]