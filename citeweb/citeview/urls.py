from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(\w+)/?(rss\.xml)?$', 'citeweb.citeview.views.index'),
)
