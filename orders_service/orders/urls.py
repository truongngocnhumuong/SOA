from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/orders/', views.create_order, name='create_order'),
    path('api/orders/list/', views.get_orders, name='get_orders'),
    path('api/orders/<int:id>/', views.get_order, name='get_order'),
    path('api/orders/<int:id>/update/', views.update_order_status, name='update_order_status'),
    path('api/order_items/', views.add_order_items, name='add_order_items'),
]