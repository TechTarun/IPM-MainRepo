from django.urls import path
from . import views
urlpatterns = [
  path('',views.index,name ="index"),
  path('proceed', views.proceed, name="proceed"),
  path('authentication', views.auth, name='auth'),
]