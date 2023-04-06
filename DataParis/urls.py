
from django.contrib import admin
from django.urls import path
from . import views

#app_name = 'DataParis'

urlpatterns = [
    path("", views.home, name="home"),
    path("", views.home, name= "temp"),
    path("Home/", views.home, name="home"),
    path("Question1.html", views.Question_1, name ="Question 1"),
    path("Question2.html", views.Question_2, name ="Question 2"),
    path("Question3.html", views.Question_3, name ="Question 3"),
    path("admin/", admin.site.urls),
]

#handler404 = 