from django.db import models

class Order(models.Model):
    """Bảng đơn hàng (orders)"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"
    
    def calculate_total(self):
        """Tính tổng tiền từ các order items"""
        total = sum(item.total_price for item in self.order_items.all())
        self.total_amount = total
        self.save()
        return total


class OrderItem(models.Model):
    """Bảng chi tiết đơn hàng (order_items)"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product_id = models.IntegerField()  # ID sản phẩm từ product service
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'order_items'
    
    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
    
    def save(self, *args, **kwargs):
        """Tự động tính total_price khi lưu"""
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        # Cập nhật tổng tiền của đơn hàng
        self.order.calculate_total()