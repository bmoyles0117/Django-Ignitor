Django Ignitor
==============

This library is intended to make the transition to Django from PHP Frameworks
such as code ignitor and the Zend Framework a bit more seamless. Django is 
one of the popular Python frameworks, but I've found that teaching newcomers
how to use it has been slightly confusing, due to Django's very flexible
approach for handling URLs to views. Some people simply want Django to take
care of the URL abstraction for them, so that it means one less thing to learn
before making the switch over.

Installation
------------

Installing "should" be super simple, just run the following command inside of this
directory from bash.

```bash
python setup.py install
```

Quick Start
-----------

Let's start off by creating a very simple IndexController, as a proof of concept. This file should be called `controllers.py` as a psuedo-standard for using this library. It's totally up to you, but following that standard will help your ability to follow documentation following this example.

```python
from django_ignitor import BaseController

class IndexController(BaseController):
    # Automatically creates urls at [/index/index, /index, and /]
    def indexAction(self, request):
        return self.respond('Hello World')
    
    # Automatically creates urls at [/index/template-test]
    def templateTestAction(self, request):
        # Exactly like you would typically use Django's render_to_response
        return self.render_to_response('some_template.html')
    
    # Automatically creates urls at [/index/autoload-template]
    # This method will search for index/autoload-template.html in your templates directory
    def autoloadTemplateAction(self, request):
        pass
```

We can then move onto the `urls.py` file, and what that should look like. A minimal version should ideally look like this, prepare to be amazed!

```python
# Import controllers to auto-discover, 100% important
from apps.example.controllers import *

# By including django ignitor's urlpatterns, you don't need to define your own!
from django_ignitor import urlpatterns
```

If you wanted to EXTEND on the urls, here's a super easy way to do that, using the django-native way!

```python
from django.conf.urls import patterns, include, url

# Import controllers to auto-discover, 100% important
from apps.example.controllers import *

from django_ignitor import urlpatterns
    
# Custom overrides if desired
urlpatterns += patterns('',
    # You can use the controllers, and grab views from them!
    url(r'custom-homepage', IndexController.get_view('indexAction')),
    
    # Or you can use what you're used to and specify your own view functions
    url(r'django-views', 'apps.example.views.hello_world'),
)
```

I hope to add plenty of documentation soon showing you how to use a few more secret sauce utilities I've built into this, but for now check out the source code, and use Django! It's truly an awesome framework with a few exceptions, but I hope this library helps you remove a few of those exceptions :)