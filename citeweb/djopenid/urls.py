
from django.conf.urls.defaults import *

urlpatterns = patterns(
    'citeweb.djopenid.views',
    (r'^(\w+)/$', 'startOpenID'),
    (r'^(\w+)/finish/$', 'finishOpenID'),
    (r'^(\w+)/xrds/$', 'rpXRDS'),
)
