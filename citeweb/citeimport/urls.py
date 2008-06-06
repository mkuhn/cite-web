from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    (r'^$', 'citeweb.citeimport.views.index'),
    (r'^save/(\w+)/?$', 'citeweb.citeimport.views.save'),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)
