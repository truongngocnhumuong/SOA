from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # Order Reports endpoints
    path('reports/orders/', views.order_reports_list, name='order-reports-list'),
    path('reports/orders/<int:pk>/', views.order_report_detail, name='order-report-detail'),
    path('reports/orders/create/', views.order_report_create, name='order-report-create'),
    path('reports/orders/<int:pk>/delete/', views.order_report_delete, name='order-report-delete'),
    
    # Product Reports endpoints
    path('reports/products/', views.product_reports_list, name='product-reports-list'),
    path('reports/products/<int:pk>/', views.product_report_detail, name='product-report-detail'),
    path('reports/products/create/', views.product_report_create, name='product-report-create'),
    path('reports/products/<int:pk>/delete/', views.product_report_delete, name='product-report-delete'),
    
    # Statistics (Bonus)
    path('reports/statistics/', views.reports_statistics, name='reports-statistics'),
]