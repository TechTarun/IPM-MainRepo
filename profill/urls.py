from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    #127.0.0.1:8000/index
    path('', views.profill, name="profill"),
]