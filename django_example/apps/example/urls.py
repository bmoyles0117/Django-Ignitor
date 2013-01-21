from django.conf.urls import patterns, include, url

# Import controllers to auto-discover, 100% important
from apps.example.controllers import *

from django_ignitor import urlpatterns
    
urlpatterns += patterns('',
    # Custom overrides if desired
    url(r'whatever/(?P<random_id>\d+)', RouteExampleController.get_view('testAction')),
    url(r'django-views', 'apps.example.views.hello_world'),
    url(r'ooblah', IndexController.get_view('indexAction'))
)
