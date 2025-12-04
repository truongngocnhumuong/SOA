from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/products/', views.get_products, name='get_products'),
    path('api/products/<int:id>/', views.get_product, name='get_product'),
    path('api/products/<int:id>/update/', views.update_product, name='update_product'),
]