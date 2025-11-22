from django.db import models

class OrderReport(models.Model):
    """Bảng báo cáo đơn hàng (orders_reports)"""
    order_id = models.IntegerField(help_text='ID đơn hàng từ Orders Service')
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='Tổng doanh thu')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='Tổng chi phí')
    total_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='Tổng lợi nhuận')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'orders_reports'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order Report #{self.id} - Order #{self.order_id}"
    
    def calculate_profit(self):
        """Tính lợi nhuận"""
        self.total_profit = self.total_revenue - self.total_cost
        return self.total_profit
    
    def save(self, *args, **kwargs):
        """Tự động tính profit khi save"""
        self.calculate_profit()
        super().save(*args, **kwargs)


class ProductReport(models.Model):
    """Bảng báo cáo sản phẩm (product_reports)"""
    order_report = models.ForeignKey(OrderReport, on_delete=models.CASCADE, related_name='product_reports')
    product_id = models.IntegerField(help_text='ID sản phẩm từ Products Service')
    product_name = models.CharField(max_length=255, blank=True, null=True)
    total_sold = models.IntegerField(default=0, help_text='Tổng số lượng đã bán')
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='Doanh thu')
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='Chi phí')
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='Lợi nhuận')
    
    class Meta:
        db_table = 'product_reports'
    
    def __str__(self):
        return f"{self.product_name} - Sold: {self.total_sold}"
    
    def calculate_profit(self):
        """Tính lợi nhuận sản phẩm"""
        self.profit = self.revenue - self.cost
        return self.profit
    
    def save(self, *args, **kwargs):
        """Tự động tính profit khi save"""
        self.calculate_profit()
        super().save(*args, **kwargs)