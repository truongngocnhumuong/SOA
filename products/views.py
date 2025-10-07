# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    # Thiết lập lớp xác thực JWT (Kiểm tra Token)
    authentication_classes = [JWTAuthentication]
    # Thiết lập phân quyền (Chỉ người dùng đã xác thực mới được CRUD)
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer