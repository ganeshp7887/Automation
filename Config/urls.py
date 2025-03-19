from . import views
from django.urls import path


def Config(request):
    instance = views.Config()
    return instance.readConfig(request)

urlpatterns = [path('', Config, name="Config")]