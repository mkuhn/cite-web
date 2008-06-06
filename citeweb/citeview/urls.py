from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(stable/)?(\w+)/?(rss\.xml)?$', 'citeweb.citeview.views.index'),
)
