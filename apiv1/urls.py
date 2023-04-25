from django.urls import path, include  
from rest_framework import routers
from . import views

app_name = 'apiv1'  

urlpatterns = [
    path('events/create/', views.CreateEventAPIView.as_view(), name="create-event"), 
    path('pays/create/', views.CreatePayAPIView.as_view(), name="create-pay"), 
    path('users/<str:user_id>/events/', views.GetEventsAPIView.as_view(), name="get-events"),
    path('events/<str:event_id>/pays/', views.GetPaysAPIView.as_view(), name="get-pays"),
    ] 

 