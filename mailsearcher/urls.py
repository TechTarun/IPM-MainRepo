from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    #127.0.0.1:8000/home
    path('', views.mailsearcher, name="mailsearcher"),
    path('listen', views.listen, name='listen'),
    path('search', views.search, name='search'),
]