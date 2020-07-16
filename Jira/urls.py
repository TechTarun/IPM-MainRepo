from django.urls import path
from . import views

urlpatterns = [
    path('', views.Jira, name="jira"),
]