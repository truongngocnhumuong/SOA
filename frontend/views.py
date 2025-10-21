from django.shortcuts import render
from django.http import JsonResponse
from user_service.models import User
from book_service.models import Book

def index(request):
    return render(request, 'index.html')

def user_detail(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        return render(request, 'user.html', {'user': user_data})
    except User.DoesNotExist:
        return render(request, 'user.html', {'error': 'Không tìm thấy người dùng'})
    except Exception as e:
        return render(request, 'user.html', {'error': f'Lỗi: {str(e)}'})

def book_detail(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        book_data = {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'available': book.available
        }
        return render(request, 'book.html', {'book': book_data})
    except Book.DoesNotExist:
        return render(request, 'book.html', {'error': 'Không tìm thấy sách'})
    except Exception as e:
        return render(request, 'book.html', {'error': f'Lỗi: {str(e)}'})
