from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home, name="Home"),
    path('Home', views.Home, name="Home"),
    path('Index', views.Home, name="Home"),
    path('Config', views.Config, name="Config"),
]