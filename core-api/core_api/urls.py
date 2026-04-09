from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import ping

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/ping/', ping, name='ping'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('api/accounts/', include('accounts.urls')),
    path('api/companies/', include('companies.urls')),
    path('api/employees/', include('employees.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/dashboard/', include('dashboard.urls')), 
]