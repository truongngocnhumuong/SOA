-- orders_database.sql
-- File SQL để tạo bảng orders và order_items
-- Đường dẫn: E:\Python_Web_SOA\myservice\orders_database.sql

-- Kiểm tra và sử dụng database hiện tại
-- Thay 'myservice_db' bằng tên database bạn đang dùng
USE myservice_db;

-- Xóa bảng cũ nếu tồn tại (cẩn thận với lệnh này!)
-- DROP TABLE IF EXISTS order_items;
-- DROP TABLE IF EXISTS orders;

-- ============================================
-- Bảng orders (Đơn hàng)
-- ============================================
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID duy nhất của đơn hàng',
    customer_name VARCHAR(255) NOT NULL COMMENT 'Tên khách hàng',
    customer_email VARCHAR(255) NOT NULL COMMENT 'Email khách hàng',
    total_amount DECIMAL(10, 2) DEFAULT 0.00 COMMENT 'Tổng số tiền của đơn hàng',
    status VARCHAR(50) DEFAULT 'pending' COMMENT 'Trạng thái: pending/completed/cancelled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Ngày tạo đơn hàng',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Ngày cập nhật',
    
    -- Indexes để tăng tốc truy vấn
    INDEX idx_status (status),
    INDEX idx_created_at (created_at),
    INDEX idx_customer_email (customer_email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Bảng đơn hàng';

-- ============================================
-- Bảng order_items (Chi tiết đơn hàng)
-- ============================================
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID duy nhất của chi tiết đơn hàng',
    order_id INT NOT NULL COMMENT 'ID đơn hàng',
    product_id INT NOT NULL COMMENT 'ID sản phẩm (liên kết với products service)',
    product_name VARCHAR(255) NOT NULL COMMENT 'Tên sản phẩm',
    quantity INT NOT NULL COMMENT 'Số lượng sản phẩm',
    unit_price DECIMAL(10, 2) NOT NULL COMMENT 'Giá sản phẩm tại thời điểm đặt',
    total_price DECIMAL(10, 2) NOT NULL COMMENT 'Tổng giá = quantity * unit_price',
    
    -- Foreign key constraint
    CONSTRAINT fk_order_items_order_id 
        FOREIGN KEY (order_id) 
        REFERENCES orders(id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    
    -- Indexes
    INDEX idx_order_id (order_id),
    INDEX idx_product_id (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Bảng chi tiết đơn hàng';

-- ============================================
-- Dữ liệu mẫu (Optional - có thể bỏ qua)
-- ============================================

-- Thêm đơn hàng mẫu
INSERT INTO orders (customer_name, customer_email, total_amount, status, created_at) VALUES
('Nguyễn Văn A', 'nguyenvana@example.com', 1500000, 'pending', NOW()),
('Trần Thị B', 'tranthib@example.com', 2500000, 'completed', DATE_SUB(NOW(), INTERVAL 1 DAY)),
('Lê Văn C', 'levanc@example.com', 800000, 'cancelled', DATE_SUB(NOW(), INTERVAL 2 DAY)),
('Phạm Thị D', 'phamthid@example.com', 3200000, 'completed', DATE_SUB(NOW(), INTERVAL 3 DAY)),
('Hoàng Văn E', 'hoangvane@example.com', 950000, 'pending', DATE_SUB(NOW(), INTERVAL 4 DAY));

-- Thêm chi tiết đơn hàng mẫu
INSERT INTO order_items (order_id, product_id, product_name, quantity, unit_price, total_price) VALUES
-- Đơn hàng #1
(1, 1, 'Laptop Dell XPS 13', 1, 1500000, 1500000),

-- Đơn hàng #2
(2, 2, 'iPhone 15 Pro', 1, 2000000, 2000000),
(2, 3, 'AirPods Pro', 1, 500000, 500000),

-- Đơn hàng #3
(3, 4, 'Samsung Galaxy S24', 1, 800000, 800000),

-- Đơn hàng #4
(4, 1, 'Laptop Dell XPS 13', 2, 1500000, 3000000),
(4, 5, 'Mouse Logitech MX', 1, 200000, 200000),

-- Đơn hàng #5
(5, 6, 'Keyboard Mechanical', 1, 950000, 950000);

-- ============================================
-- Kiểm tra dữ liệu
-- ============================================
SELECT 'Orders table created successfully!' as message;
SELECT COUNT(*) as total_orders FROM orders;
SELECT COUNT(*) as total_order_items FROM order_items;

-- Xem dữ liệu vừa tạo
SELECT * FROM orders;
SELECT * FROM order_items;