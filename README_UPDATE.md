# Cập nhật chức năng xem và sửa người dùng/sách

## Tổng quan
Đã cập nhật thêm chức năng xem và sửa chi tiết người dùng và sách cho hệ thống Library SOA.

## Các thay đổi chính

### 1. Backend (Views)
- **frontend/views.py**: Thêm `user_detail()` và `book_detail()` views
- **frontend/urls.py**: Thêm routes cho `/user/<id>/` và `/book/<id>/`

### 2. Frontend Templates
- **user.html**: Template chi tiết người dùng với chức năng sửa inline
- **book.html**: Template chi tiết sách với chức năng sửa inline
- **app.js**: Thêm nút "Xem" và cải thiện chức năng sửa

### 3. Chức năng mới
- **Xem chi tiết**: Click nút "Xem" để xem thông tin chi tiết
- **Sửa inline**: Sửa trực tiếp trên trang chi tiết
- **Sửa nhanh**: Sửa trực tiếp từ danh sách chính
- **Xóa**: Xóa với xác nhận

## Cách sử dụng

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Chạy Django project
```bash
# Chạy tất cả services trên một instance (SOA Architecture)
python manage.py runserver 8000
```

### 3. Truy cập ứng dụng
- Frontend: http://127.0.0.1:8000/
- User API: http://127.0.0.1:8000/api/user/users/
- Book API: http://127.0.0.1:8000/api/book/books/

### 4. Test chức năng
```bash
python test_functionality.py
```

## Tính năng mới

### Trang chủ (index.html)
- **Tab Người dùng**: Nút "Xem", "Sửa", "Xóa" cho mỗi người dùng
- **Tab Sách**: Nút "Xem", "Sửa", "Xóa" cho mỗi sách  
- **Tab Mượn sách**: 
  - Dropdown chọn người dùng (hiển thị tên + email)
  - Dropdown chọn sách (hiển thị tên + tác giả + trạng thái)
  - Sách không có sẵn sẽ bị disable
  - Hiển thị danh sách mượn với tên thay vì ID

### Trang chi tiết người dùng (/user/<id>/)
- Hiển thị đầy đủ thông tin: ID, username, email, ngày tạo
- Sửa inline từng trường
- Xóa người dùng
- Nút quay lại trang chủ

### Trang chi tiết sách (/book/<id>/)
- Hiển thị đầy đủ thông tin: ID, tên sách, tác giả, trạng thái
- Sửa inline từng trường
- Thay đổi trạng thái có sẵn/không có sẵn
- Xóa sách
- Nút quay lại trang chủ

## API Endpoints mới

### Frontend URLs
- `GET /user/<int:user_id>/` - Xem chi tiết người dùng
- `GET /book/<int:book_id>/` - Xem chi tiết sách

### API Endpoints (đã có sẵn)
- `GET /api/user/users/` - Danh sách người dùng
- `POST /api/user/users/` - Tạo người dùng
- `GET /api/user/users/<id>/` - Xem người dùng
- `PUT /api/user/users/<id>/` - Sửa người dùng
- `DELETE /api/user/users/<id>/` - Xóa người dùng

- `GET /api/book/books/` - Danh sách sách
- `POST /api/book/books/` - Tạo sách
- `GET /api/book/books/<id>/` - Xem sách
- `PUT /api/book/books/<id>/` - Sửa sách
- `DELETE /api/book/books/<id>/` - Xóa sách

## Kiến trúc SOA
- **Service Layer**: Mỗi service (user_service, book_service, borrow_service) là một Django app riêng biệt
- **API Gateway**: Tất cả API được expose qua main Django project (`/api/user/`, `/api/book/`, `/api/borrow/`)
- **Frontend**: Chỉ giao tiếp với API Gateway, không kết nối trực tiếp đến service
- **Database**: Shared database (SQLite) cho tất cả services
- **Deployment**: Single instance chạy tất cả services

## Lưu ý
- Chỉ cần chạy một Django instance duy nhất
- Các thay đổi được lưu ngay lập tức vào database
- Giao diện responsive với Bootstrap 5
- Hỗ trợ tiếng Việt
- Tuân thủ kiến trúc SOA với API Gateway
