from django.urls import path, include
from . import views
from django.contrib import admin
from django.conf import settings

admin.site.site_header = settings.ADMIN_SITE_HEADER

urlpatterns = [
    path('', views.EmployeesView.as_view()),
    path('phone_book/', views.PhonebookView.as_view()),
    path('comp_isod/', views.CompIsodView.as_view()),
    path('analytics_ic/', views.AnalyticsIc.as_view()),
    path('download_lists/', views.DownloadListsView.as_view()),
    path('download_lists/export/excel', views.DownloadListsView.get_xlsx_emp_all),
    path('download_lists/export/get_xlsx_arm_isod', views.DownloadListsView.get_xlsx_arm_isod),
    path('accounts/', include('django.contrib.auth.urls')),
    path('<slug:slug>/', views.EmployeesDetailView.as_view(), name='employee_detail'),
]
