from django.urls import path
from . import views

urlpatterns = [
    path('', views.EmployeesBirthMonth.as_view())
]