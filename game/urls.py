from django.conf.urls import patterns, url
from game import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^register/$', views.register, name='register'),
		url(r'^leaderboards/$', views.leaderboards, name='leaderboards'))



