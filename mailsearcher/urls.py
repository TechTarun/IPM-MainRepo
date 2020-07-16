from django.urls import path
from . import views

urlpatterns = [

    path('', views.mailsearcher, name="mailsearcher"),
    path('listen', views.listen, name='listen'),
    path('search', views.search, name='search'),
]