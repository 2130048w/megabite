from django.conf.urls import patterns, url
from game import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.myLogin, name='myLogin'),
        url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^leaderboards/$', views.leaderboards, name='leaderboards'),
        url(r'^intro/$', views.intro, name='intro'),
        url(r'^play/$', views.game, name='game'),
        url(r'^safehouse/$', views.safehouse, name='safehouse'),
	url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
                       )
		



