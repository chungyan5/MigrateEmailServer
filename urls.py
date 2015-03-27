from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MigrateEmailServer.views.home', name='home'),
    #	 get logic app:
    url(r'^MigrateEmailServer/', include('getlogin.urls')),
    #url(r'', include('getlogin.urls'))

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^MigrateEmailServer/admin/', include(admin.site.urls)),
)
