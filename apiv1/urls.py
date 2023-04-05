from django.urls import path, include  
from rest_framework import routers
from . import views  

app_name = 'apiv1'  

urlpatterns = [
    path('create-event/', views.CreateEventAPIView, "create-event"),  
    ] 

 