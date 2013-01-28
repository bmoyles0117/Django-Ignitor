from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import importlib

import os

class Command(BaseCommand):
    args = ''
    help = 'Remove some of the mundane boilerplate items necessary when working with django'
    
    def handle(self, *args, **options):
        settings_module = importlib.import_module(settings.SETTINGS_MODULE)
        
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