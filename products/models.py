from django.db import models

class Product(models.Model):
    # id (PRIMARY KEY) được Django tự động tạo ra
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2) # DECIMAL(10, 2)
    quantity = models.IntegerField(default=0) # INT
    # TIMESTAMP fields - Django tự động quản lý
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name
