from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^import/', include('citeweb.citeimport.urls')),
    (r'^view/', include('citeweb.citeview.urls')),

    (r'^$', 'citeweb.citeview.views.index'),
)
