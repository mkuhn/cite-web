from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(stable/)?(\w{10,})?/?(rss\.xml)?$', 'citeweb.citeview.views.index'),
)
