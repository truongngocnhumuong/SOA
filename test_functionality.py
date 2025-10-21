#!/usr/bin/env python
"""
Script để test chức năng xem và sửa người dùng/sách
"""
import requests
import json

# URLs của các service (qua API Gateway)
USER_API = "http://127.0.0.1:8000/api/user/users/"
BOOK_API = "http://127.0.0.1:8000/api/book/books/"
FRONTEND_URL = "http://127.0.0.1:8000/"

def test_user_operations():
    print("=== TESTING USER OPERATIONS ===")
    
    # Tạo user mới
    user_data = {
        "username": "test_user",
        "email": "test@example.com"
    }
    
    try:
        response = requests.post(USER_API, json=user_data)
        if response.status_code == 201:
            user = response.json()
            print(f"✅ Tạo user thành công: {user}")
            user_id = user['id']
            
            # Test xem user
            response = requests.get(f"{USER_API}{user_id}/")
            if response.status_code == 200:
                print(f"✅ Xem user thành công: {response.json()}")
            else:
                print(f"❌ Lỗi xem user: {response.status_code}")
            
            # Test sửa user
            update_data = {
                "username": "updated_user",
                "email": "updated@example.com"
            }
            response = requests.put(f"{USER_API}{user_id}/", json=update_data)
            if response.status_code == 200:
                print(f"✅ Sửa user thành công: {response.json()}")
            else:
                print(f"❌ Lỗi sửa user: {response.status_code}")
            
            # Test xóa user
            response = requests.delete(f"{USER_API}{user_id}/")
            if response.status_code == 204:
                print("✅ Xóa user thành công")
            else:
                print(f"❌ Lỗi xóa user: {response.status_code}")
                
        else:
            print(f"❌ Lỗi tạo user: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")

def test_book_operations():
    print("\n=== TESTING BOOK OPERATIONS ===")
    
    # Tạo book mới
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "available": True
    }
    
    try:
        response = requests.post(BOOK_API, json=book_data)
        if response.status_code == 201:
            book = response.json()
            print(f"✅ Tạo book thành công: {book}")
            book_id = book['id']
            
            # Test xem book
            response = requests.get(f"{BOOK_API}{book_id}/")
            if response.status_code == 200:
                print(f"✅ Xem book thành công: {response.json()}")
            else:
                print(f"❌ Lỗi xem book: {response.status_code}")
            
            # Test sửa book
            update_data = {
                "title": "Updated Book",
                "author": "Updated Author",
                "available": False
            }
            response = requests.put(f"{BOOK_API}{book_id}/", json=update_data)
            if response.status_code == 200:
                print(f"✅ Sửa book thành công: {response.json()}")
            else:
                print(f"❌ Lỗi sửa book: {response.status_code}")
            
            # Test xóa book
            response = requests.delete(f"{BOOK_API}{book_id}/")
            if response.status_code == 204:
                print("✅ Xóa book thành công")
            else:
                print(f"❌ Lỗi xóa book: {response.status_code}")
                
        else:
            print(f"❌ Lỗi tạo book: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")

def test_borrow_operations():
    print("\n=== TESTING BORROW OPERATIONS ===")
    
    try:
        # Test tạo borrow mới
        borrow_data = {
            "user": 1,
            "book": 1,
            "borrow_date": "2025-10-21"
        }
        
        response = requests.post("http://127.0.0.1:8000/api/borrow/borrows/", json=borrow_data)
        if response.status_code == 201:
            borrow = response.json()
            print(f"✅ Tạo borrow thành công: {borrow}")
            borrow_id = borrow['id']
            
            # Test xem borrow
            response = requests.get(f"http://127.0.0.1:8000/api/borrow/borrows/{borrow_id}/")
            if response.status_code == 200:
                print(f"✅ Xem borrow thành công: {response.json()}")
            else:
                print(f"❌ Lỗi xem borrow: {response.status_code}")
            
            # Test xóa borrow
            response = requests.delete(f"http://127.0.0.1:8000/api/borrow/borrows/{borrow_id}/")
            if response.status_code == 204:
                print("✅ Xóa borrow thành công")
            else:
                print(f"❌ Lỗi xóa borrow: {response.status_code}")
                
        else:
            print(f"❌ Lỗi tạo borrow: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")

def test_frontend_urls():
    print("\n=== TESTING FRONTEND URLS ===")
    
    try:
        # Test trang chủ
        response = requests.get(FRONTEND_URL)
        if response.status_code == 200:
            print("✅ Trang chủ frontend hoạt động")
        else:
            print(f"❌ Lỗi trang chủ: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Lỗi kết nối frontend: {e}")

if __name__ == "__main__":
    print("🚀 Bắt đầu test chức năng...")
    print("⚠️  Lưu ý: Đảm bảo Django project đang chạy:")
    print("   - Main project: python manage.py runserver 8000")
    print("   - Tất cả services chạy trên cùng một instance")
    print()
    
    test_user_operations()
    test_book_operations()
    test_borrow_operations()
    test_frontend_urls()
    
    print("\n✅ Hoàn thành test!")
