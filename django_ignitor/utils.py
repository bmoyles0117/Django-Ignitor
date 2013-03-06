from .shared import urlpatterns
from django.conf.urls import patterns, url
from django.shortcuts import HttpResponse, render, redirect, render_to_response

import functools
import inspect
import re
import simplejson
 
_underscorer1 = re.compile(r'(.)([A-Z][a-z]+)')
_underscorer2 = re.compile('([a-z0-9])([A-Z])')
 
def camel_to_tabs(s):
    subbed = _underscorer1.sub(r'\1-\2', s)
    return _underscorer2.sub(r'\1-\2', subbed).lower()

class BaseControllerMetaclass(type):
    def __new__(cls, name, bases, dct):
        global urlpatterns
        
        instance = type.__new__(cls, name, bases, dct)
        
        # Copy the Meta definition to a local var
        instance._meta = instance.Meta()
        
        # Ignore the base controller, so routes don't get added
        if name != 'BaseController':
            # Clean up the controller name, zend style
            controller_name = camel_to_tabs(name.replace('Controller', '')).lower()

            # Filter out callable actions by their naming conventions and functionality
            methods = [x for x in inspect.getmembers(instance, predicate=inspect.ismethod) if 'Action' in x[0]]
            
            for method_name, method_function in methods:
                # Clean up the action name, zend style
                action_name = camel_to_tabs(method_name.replace('Action', '')).lower()
                
                # Request the processor partial to be applied to the URL dispatcher
                callable = instance().request_processor(method_function)
                
                # Collect the route regex from the controller, to be inserted into the URL dispatcher
                base_route = instance._meta.route
                
                # Make a linkable alias for django's url template helper
                linkable_alias = '%s.%s.%s' % (instance.__module__, controller_name, action_name, )
                
                # Add the primary route, hotswapping keywords for their dynamic replacements
                urls = [url(base_route.replace(':controller', controller_name).replace(':action', action_name), callable, name=linkable_alias)]
                
                # If we're working with an Index[Controller|Action], we need to create special routes
                if controller_name == 'index' and action_name == 'index':
                    urls += [url(r'^$', callable, name=linkable_alias)]
                if action_name == 'index':
                    urls += [url(r'^%s$' % controller_name, callable, name=linkable_alias)]

                # Add the collection of URL routes to the URL Dispatcher
                urlpatterns += patterns('', *urls)
                        
        return instance

def template_finder(instance, method, *args, **kwargs):
    """Check to see if the view returned a response, if it didn't then we should 
    automagically return a render_to_response with an appropriate 
    /controller/action.html that corresponds with the view that was called.
    
    Keyword Arguments:
    instance -- the controller instance where the method can be discovered
    method -- the method / view being called to render the response
    *args && **kwargs -- proxied directly to the method being called
    """
    method_response = method(instance, *args, **kwargs)
    
    controller_name = camel_to_tabs(instance.__class__.__name__.replace('Controller', '')).lower()
    action_name = camel_to_tabs(method.__name__.replace('Action', '')).lower()
    
    # If the method does not return a response, build one for it
    if not method_response:
        return instance.render(args[0], '%s%s/%s.html' % (
            getattr(instance._meta, 'template_root', ''),
            controller_name, 
            action_name, 
        ), instance.template_dict)
    
    return method_response

class BaseController(object):
    __metaclass__ = BaseControllerMetaclass
    
    class Meta:
        route = r'^:controller/:action$'
        template_root = ''
    
    def __init__(self):
        self.template_dict = {}
        
    @classmethod
    def get_view(cls, method_name):
        """Django shortcut to get a view method to use in the URL Dispatcher"""
        return cls().request_processor(getattr(cls, method_name))
    
    def redirect(self, *args, **kwargs):
        """Proxy to Django redirect method"""
        return redirect(*args, **kwargs)
            
    def render(self, *args, **kwargs):
        """Proxy to Django render method"""
        return render(*args, **kwargs)
            
    def render_to_response(self, *args, **kwargs):
        """Proxy to Django render_to_response method"""
        return render_to_response(*args, **kwargs)
    
    def render_json(self, json_dict):
        """A quick shortcut to return JSON quickly and easily from a dict"""
        return HttpResponse(simplejson.dumps(json_dict), content_type="application/json")

    def request_processor(self, method):
        """Returns a partially invoked method to return a response when invoked"""
        return functools.partial(template_finder, self, method)
    
    def respond(self, *args, **kwargs):
        """Proxy to Django HttpResponse class"""
        return HttpResponse(*args, **kwargs)