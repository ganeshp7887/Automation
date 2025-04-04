from Instore_Testing import views
from django.urls import path


def instore_testing_view(request):
    instance = views.InstoreTesting()
    return instance.Instore_Testing(request)

def bypass(request):
    instance = views.InstoreTesting()
    return instance.bypass(request)

def Single_Instore_Testing(request):
    instance = views.InstoreTesting()
    return instance.Single_Instore_Testing(request)

urlpatterns = [ path('Instore_Testing', instore_testing_view, name='Instore_Testing'),
                path('Single_Instore_Testing', Single_Instore_Testing, name="Single_Instore_Testing"),
                path('bypass', bypass, name='bypass')]