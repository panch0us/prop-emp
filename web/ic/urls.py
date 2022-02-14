from django.urls import path
from . import views

urlpatterns = [
    path('', views.EmployeesView.as_view()),
    path('<slug:slug>/', views.EmployeesDetailView.as_view(), name='employee_detail')
]