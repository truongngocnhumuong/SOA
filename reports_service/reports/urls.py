from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Order Reports
    path('api/reports/orders/', views.create_order_report, name='create_order_report'),
    path('api/reports/orders/list/', views.get_order_reports, name='get_order_reports'),
    path('api/reports/orders/stats/', views.get_order_stats, name='get_order_stats'),
    path('api/reports/orders/<int:id>/', views.get_order_report, name='get_order_report'),
    
    # Product Reports
    path('api/reports/products/', views.create_product_report, name='create_product_report'),
    path('api/reports/products/list/', views.get_product_reports, name='get_product_reports'),
    path('api/reports/products/stats/', views.get_product_stats, name='get_product_stats'),
    path('api/reports/products/<int:id>/', views.get_product_report, name='get_product_report'),
    
    # Dashboard
    path('api/reports/dashboard/', views.dashboard, name='dashboard'),
]