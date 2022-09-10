from django.urls import path
from . import views

urlpatterns = [
    path('messages/<slug:pk>', views.Messages.as_view()),
    path('login', views.Login.as_view())
]