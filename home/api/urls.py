from home.views import index, people

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('index/', index),
    path('people/', people),
]
