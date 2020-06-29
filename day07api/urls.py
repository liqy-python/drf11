from django.urls import path

from day07api import views

urlpatterns = [
    path("emp/", views.EmployeeAPIView.as_view()),
    path("emp/<str:pk>/", views.EmployeeAPIView.as_view()),
]