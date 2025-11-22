# URLs riêng cho Reporting Service

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'service': 'reporting-service',
        'port': 8003
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check),
    path('', include('reports.urls')),  # Chỉ reports URLs
]