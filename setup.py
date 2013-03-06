#!/usr/bin/env python

from setuptools import setup

setup(
    name='Django Ignitor',
    version='0.095',
    description='Giving Django an MVC Framework layer',
    author='Bryan Moyles',
    author_email='bryan.moyles@teltechcorp.com',
    packages=['django_ignitor', 'django_ignitor.management', 'django_ignitor.management.commands'],
    url='',
    install_requires=[
        'simplejson==3.0.7', 
        'django', 
        'telapi',
    ]
)
