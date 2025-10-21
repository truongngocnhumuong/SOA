from rest_framework import serializers
from .models import Borrow

class BorrowSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    
    class Meta:
        model = Borrow
        fields = ['id', 'user', 'book', 'user_name', 'book_title', 'borrow_date', 'return_date']