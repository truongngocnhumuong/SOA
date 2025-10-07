from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # 'id' là trường mặc định nên không cần thêm vào fields
        fields = ['id', 'name', 'description', 'price', 'quantity', 'created_at', 'updated_at']
        # Thiết lập các trường chỉ đọc để không bị cập nhật từ API POST/PUT
        read_only_fields = ['created_at', 'updated_at']