from django.urls import path, include  
from rest_framework import routers
from . import views

app_name = 'apiv1'

urlpatterns = [
    path('events/', views.CreateEventAPIView.as_view(), name="create-event"), 
    path('pays/', views.CreatePayAPIView.as_view(), name="create-pay"), 
    path('users/<str:user_id>/events/', views.GetEventsAPIView.as_view(), name="get-events"),
    path('events/<str:event_id>/pays/', views.GetPaysAPIView.as_view(), name="get-pays"),
    path('qr/', views.ReadQrAPIView.as_view(), name="read-qr"),
    path('events/<str:event_id>/adjustment/', views.AdjustEventAPIView.as_view(), name="adjust-events"),
    path('friends/', views.RequestFriendAPIView.as_view(), name="request-friends"),
    path('friends/<str:friend_id>/approval/', views.ApproveFriendAPIView.as_view(), name="approve-friends"),
    ] 