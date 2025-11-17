from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer cho OrderItem"""
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product_id', 'product_name', 'quantity', 
                  'unit_price', 'total_price']
        read_only_fields = ['total_price']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer cho Order với danh sách items"""
    order_items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'customer_email', 'total_amount', 
                  'status', 'created_at', 'updated_at', 'order_items']
        read_only_fields = ['total_amount', 'created_at', 'updated_at']


class CreateOrderSerializer(serializers.Serializer):
    """Serializer cho việc tạo đơn hàng mới"""
    customer_name = serializers.CharField(max_length=255)
    customer_email = serializers.EmailField()
    items = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        help_text="Danh sách sản phẩm: [{'product_id': 1, 'quantity': 2}, ...]"
    )
    
    def validate_items(self, value):
        """Validate items data"""
        if not value:
            raise serializers.ValidationError("Đơn hàng phải có ít nhất 1 sản phẩm")
        
        for item in value:
            if 'product_id' not in item:
                raise serializers.ValidationError("Mỗi sản phẩm phải có product_id")
            if 'quantity' not in item:
                raise serializers.ValidationError("Mỗi sản phẩm phải có quantity")
            
            try:
                item['product_id'] = int(item['product_id'])
                item['quantity'] = int(item['quantity'])
            except (ValueError, TypeError):
                raise serializers.ValidationError("product_id và quantity phải là số nguyên")
            
            if item['quantity'] <= 0:
                raise serializers.ValidationError("Quantity phải lớn hơn 0")
        
        return value