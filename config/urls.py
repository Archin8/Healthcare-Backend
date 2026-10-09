from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include


def api_root_view(request):
    return JsonResponse({
        "message": "Welcome to Healthcare REST API",
        "status": "online",
        "admin_panel": "/admin/",
        "endpoints": {
            "auth_register": "POST /api/auth/register/",
            "auth_login": "POST /api/auth/login/",
            "patients": "GET/POST /api/patients/",
            "doctors": "GET/POST /api/doctors/",
            "mappings": "GET/POST /api/mappings/"
        }
    })


urlpatterns = [
    path('', api_root_view, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/', include('patients.urls')),
    path('api/', include('doctors.urls')),
    path('api/', include('mappings.urls')),
]

