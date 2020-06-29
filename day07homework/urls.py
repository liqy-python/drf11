from django.urls import path

from day07homework import views

urlpatterns = [
    path("stu/", views.StudentAPIView.as_view()),
    path("stu/<str:pk>/", views.StudentAPIView.as_view()),
]