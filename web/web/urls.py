from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('ic/', include('ic.urls')),
    path('admin/', admin.site.urls),
]
