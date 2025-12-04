from django.db import models
from django.utils import timezone

class OrderReport(models.Model):
    order_id = models.IntegerField()
    customer_name = models.CharField(max_length=200, default='')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Report for Order {self.order_id}"

class ProductReport(models.Model):
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=200, default='')
    total_sold = models.IntegerField()
    revenue = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Report for Product {self.product_id}"
    
    @property
    def profit(self):
        return self.revenue - self.cost