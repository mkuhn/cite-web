from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    (r'^import/', include('citeweb.citeimport.urls')),
    (r'^view/', include('citeweb.citeview.urls')),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)
