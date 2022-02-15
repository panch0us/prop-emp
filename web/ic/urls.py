from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.EmployeesView.as_view()),
    path('phone_book/', views.PhonebookView.as_view()),
    path('accounts/', include('django.contrib.auth.urls')),
    path('<slug:slug>/', views.EmployeesDetailView.as_view(), name='employee_detail')

]