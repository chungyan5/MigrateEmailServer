from django.conf.urls.defaults import patterns, include, url
import getlogin 

urlpatterns = patterns('',

    url(r'^$', 'getlogin.views.home', name='home'),
    url(r'^list', 'getlogin.views.list', name='list'),
    #url(r'^post/(?P<pk>[0-9]+)/$', 'getlogin.views.migrating', name='migrating'),
)
