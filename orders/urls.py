from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Order endpoints
    path('orders/', views.order_list, name='order-list'),
    path('orders/<int:pk>/', views.order_detail, name='order-detail'),
    path('orders/create/', views.order_create, name='order-create'),
    path('orders/<int:pk>/update/', views.order_update, name='order-update'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order-delete'),
    
    # Order Item endpoints
    path('order_items/', views.order_item_list, name='order-item-list'),
    path('order_items/<int:pk>/', views.order_item_detail, name='order-item-detail'),
    path('order_items/create/', views.order_item_create, name='order-item-create'),
    path('order_items/<int:pk>/update/', views.order_item_update, name='order-item-update'),
    path('order_items/<int:pk>/delete/', views.order_item_delete, name='order-item-delete'),
]