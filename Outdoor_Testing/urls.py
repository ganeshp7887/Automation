from django.urls import path

from . import views

def outdoor_testing_view(request):
    instance = views.OutdoorTesting()
    return instance.Outdoor_Testing(request)

def single_outdoor_testing(request):
    instance = views.OutdoorTesting()
    return instance.Single_Outdoor_Testing(request)

urlpatterns = [ path('Outdoor_Testing', outdoor_testing_view, name='Outdoor_Testing'),
                path('Single_Outdoor_Testing', single_outdoor_testing, name="Single_Outdoor_Testing")]
