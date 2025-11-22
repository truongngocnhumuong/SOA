from rest_framework import serializers
from .models import OrderReport, ProductReport

class ProductReportSerializer(serializers.ModelSerializer):
    """Serializer cho ProductReport"""
    class Meta:
        model = ProductReport
        fields = ['id', 'order_report', 'product_id', 'product_name', 
                  'total_sold', 'revenue', 'cost', 'profit']
        read_only_fields = ['profit']


class OrderReportSerializer(serializers.ModelSerializer):
    """Serializer cho OrderReport với danh sách product reports"""
    product_reports = ProductReportSerializer(many=True, read_only=True)
    
    class Meta:
        model = OrderReport
        fields = ['id', 'order_id', 'total_revenue', 'total_cost', 
                  'total_profit', 'created_at', 'updated_at', 'product_reports']
        read_only_fields = ['total_profit', 'created_at', 'updated_at']


class CreateOrderReportSerializer(serializers.Serializer):
    """Serializer để tạo báo cáo đơn hàng từ Orders Service"""
    order_id = serializers.IntegerField(help_text='ID đơn hàng cần tạo báo cáo')
    
    def validate_order_id(self, value):
        """Validate order_id"""
        if value <= 0:
            raise serializers.ValidationError("order_id phải lớn hơn 0")
        return value


class CreateProductReportSerializer(serializers.Serializer):
    """Serializer để tạo báo cáo sản phẩm"""
    product_id = serializers.IntegerField(help_text='ID sản phẩm cần tạo báo cáo')
    start_date = serializers.DateField(required=False, help_text='Ngày bắt đầu (optional)')
    end_date = serializers.DateField(required=False, help_text='Ngày kết thúc (optional)')
    
    def validate_product_id(self, value):
        """Validate product_id"""
        if value <= 0:
            raise serializers.ValidationError("product_id phải lớn hơn 0")
        return value