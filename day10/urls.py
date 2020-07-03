from django.urls import path

from day10 import views

urlpatterns = [
    path("test/", views.TestAPIView.as_view()),
    path("auth/", views.TestPermission.as_view()),
    path("user/", views.UserLogin.as_view()),
    path("send/", views.SendMessageAPIView.as_view()),

]