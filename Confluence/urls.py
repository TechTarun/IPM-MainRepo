from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    #127.0.0.1:8000/home
    path('', views.Confluence, name="Confluence"),
]