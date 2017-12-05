from django.conf.urls import url
from blog import views



urlpatterns = [

    url(r'^poll/',views.poll),
    url(r'^comment/', views.comment),
    url(r'^backendIndex/',views.backendIndex),
    url(r'^backend/addArticle/', views.addArticle),

    url(r'^commentTree/(?P<article_id>\d+)/',views.commentTree),
    url(r'^(?P<username>.*)/(?P<condition>category|tag|archive)/(?P<para>.*)/',views.homeSite),
    url(r'^(?P<username>.*)/articles/(?P<article_id>\d+)/',views.articleDetail),
    url(r'^(?P<username>.*)/',views.homeSite),
]
