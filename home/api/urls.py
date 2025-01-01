from home.views import index, people, signup, Student, register

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('index/', index),
    path('people/', people),
    path('signup/', signup),
    path('student/', Student.as_view()),
    path('register/', register.as_view()),
]
