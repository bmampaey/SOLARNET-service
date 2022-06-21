'''Module to customize the default admin app for the project, done in a way to reimplement as little from the django.contrib.admin app'''
from django.contrib.admin import action, ModelAdmin
from .site import register
