from django.contrib import admin
from .models import OrderReport, ProductReport

@admin.register(OrderReport)
class OrderReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id', 'customer_name', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_id', 'customer_name']
    ordering = ['-created_at']

@admin.register(ProductReport)
class ProductReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_id', 'product_name', 'total_sold', 'revenue', 'cost', 'get_profit', 'created_at']
    list_filter = ['created_at']
    search_fields = ['product_id', 'product_name']
    ordering = ['-total_sold']
    
    def get_profit(self, obj):
        return f"{obj.profit:,.0f} VND"
    get_profit.short_description = 'Lợi nhuận'