
from django.contrib import admin
from django.urls import path
from . import views

#app_name = 'main'

urlpatterns = [
    path("", views.home, name="home"),
    #path("", views.home, name="temp"),
    path("Question_1/", views.Question_1, name="Q1"),
    path("Question_2/", views.Question_2, name="Q2"),
    path("Question_3/", views.Question_3, name="Q3"),
]
