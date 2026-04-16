import os
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include, re_path 
from django.views.generic import TemplateView  
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import ping
from django.conf import settings
from django.conf.urls.static import static

# A simple view to serve the index file
def render_vue(request):
    index_path = os.path.join(settings.BASE_DIR, 'dist', 'index.html')
    try:
        with open(index_path, 'r') as f:
            return HttpResponse(f.read())
    except FileNotFoundError:
        return HttpResponse("Vue build not found. Did you run npm run build?", status=404)

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

    re_path(r'^.*$', render_vue),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)