from django.urls import path
from . import views

urlpatterns = [
    path('', views.Github, name="Github"),
    path('listen', views.listen, name='listen_github'),
    path('search', views.search, name='search_github'),
]