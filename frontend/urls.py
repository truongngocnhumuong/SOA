from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
]
