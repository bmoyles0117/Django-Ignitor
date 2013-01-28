from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import importlib

import os

class Command(BaseCommand):
    args = ''
    help = 'Remove some of the mundane boilerplate items necessary when working with django'
    
    def handle(self, *args, **options):
        print settings.SETTINGS_MODULE
        
        settings_module = importlib.import_module(settings.SETTINGS_MODULE)
        
        application_module = settings.SETTINGS_MODULE.replace('.settings', '')
        
        settings_file = settings_module.__file__
        
        if settings_file.endswith('.pyc'):
            settings_file = settings_file.replace('.pyc', '.py')
            
        settings_directory = os.path.realpath(os.path.dirname(settings_file))
        
        if hasattr(settings_module, 'SITE_ROOT'):
            print "Settings module already has SITE_ROOT declared, no work necessary"
        else:
            with open(settings_file, 'a+') as settings_handler:
                settings_handler.write("""
import os

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

TEMPLATE_DIRS += (
    '%s/templates' % SITE_ROOT,
)
""")
            
            print "Settings module has been successfully simplified"
        
        
        if os.path.isdir('%s/templates' % settings_directory):
            print "Templates directory already existed, no creation was necessary"
        else:
            os.mkdir('%s/templates' % settings_directory)
            
            print "Templates directory has been created at %s/templates" % settings_directory
        
        if os.path.isfile('%s/controllers.py' % settings_directory):
            print "Controller module already exists, no work necessary"
        else:
            with open('%s/controllers.py' % settings_directory, 'w+') as controllers_handler:
                controllers_handler.write('from django_ignitor import BaseController')
        
        urls_module = importlib.import_module('%s.urls' % application_module)
        
        overwrite_urls = False
        
        try:
            print urls_module.urlpatterns
            print len(urls_module.urlpatterns)
            
            if len(urls_module.urlpatterns) == 0:
                overwrite_urls = True
        except AttributeError, e:
            overwrite_urls = True
        
        if overwrite_urls:
            print "Overwriting the urls.py file, being that no urlpatterns have been defined"
            
            with open('%s/urls.py' % settings_directory, 'w+') as urls_handler:
                urls_handler.write("""from django.conf.urls import patterns, include, url
from django_ignitor import urlpatterns
from controllers import *

urlpatterns += patterns('',
    # Examples:
    # url(r'^$', '%s.views.home', name='home'),
    # url(r'^%s/', include('%s.foo.urls')),
)""" % (application_module, application_module, application_module, ))
        else:
            print "Appending to the urls.py file, being that urlpatterns have already been defined"
            
            with open('%s/urls.py' % settings_directory, 'a+') as urls_handler:
                urls_handler.write("""

from django_ignitor import urlpatterns as ignitor_urlpatterns
from controllers import *

urlpatterns = ignitor_urlpatterns + urlpatterns
""")
            