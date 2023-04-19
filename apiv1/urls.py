from django.urls import path, include  
from rest_framework import routers
from . import views

app_name = 'apiv1'  

urlpatterns = [
    path('create-event/', views.CreateEventAPIView.as_view(), name="create-event"), 
    path('create-pay/', views.CreatePayAPIView.as_view(), name="create-pay"), 
    path('get-events/', views.GetEventsAPIView.as_view(), name="get-events"),
    path('get-pays/', views.GetPaysAPIView.as_view(), name="get-pays"),
    ] 

 