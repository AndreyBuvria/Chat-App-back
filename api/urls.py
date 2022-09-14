from django.urls import path
from . import views

urlpatterns = [
    path('rooms', views.Rooms.as_view()),
    path('messages/<slug:pk>', views.Messages.as_view()),
    path('login', views.Login.as_view()),
]