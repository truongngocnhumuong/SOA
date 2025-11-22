-- reporting_database.sql
-- Database riêng cho Reporting Service
-- Chạy trong MySQL Workbench hoặc MySQL Command Line

-- Tạo database mới
CREATE DATABASE IF NOT EXISTS reporting_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE reporting_db;

-- ============================================
-- Bảng orders_reports (Báo cáo đơn hàng)
-- ============================================
CREATE TABLE IF NOT EXISTS orders_reports (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID của báo cáo đơn hàng',
    order_id INT NOT NULL COMMENT 'ID đơn hàng từ Orders Service',
    total_revenue DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT 'Tổng doanh thu',
    total_cost DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT 'Tổng chi phí',
    total_profit DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT 'Tổng lợi nhuận',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Ngày tạo báo cáo',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Ngày cập nhật',
    
    -- Indexes
    INDEX idx_order_id (order_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Bảng báo cáo đơn hàng';

-- ============================================
-- Bảng product_reports (Báo cáo sản phẩm)
-- ============================================
CREATE TABLE IF NOT EXISTS product_reports (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID của báo cáo sản phẩm',
    order_report_id INT NOT NULL COMMENT 'ID báo cáo đơn hàng',
    product_id INT NOT NULL COMMENT 'ID sản phẩm từ Products Service',
    product_name VARCHAR(255) COMMENT 'Tên sản phẩm',
    total_sold INT NOT NULL DEFAULT 0 COMMENT 'Tổng số lượng đã bán',
    revenue DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT 'Doanh thu',
    cost DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT 'Chi phí',
    profit DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT 'Lợi nhuận',
    
    -- Foreign key
    CONSTRAINT fk_product_reports_order_report_id 
        FOREIGN KEY (order_report_id) 
        REFERENCES orders_reports(id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    
    -- Indexes
    INDEX idx_order_report_id (order_report_id),
    INDEX idx_product_id (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Bảng báo cáo sản phẩm';

-- ============================================
-- Dữ liệu mẫu (Optional)
-- ============================================

-- Báo cáo đơn hàng mẫu
INSERT INTO orders_reports (order_id, total_revenue, total_cost, total_profit) VALUES
(1, 1500000, 1200000, 300000),
(2, 2500000, 2000000, 500000),
(3, 800000, 650000, 150000);

-- Báo cáo sản phẩm mẫu
INSERT INTO product_reports (order_report_id, product_id, product_name, total_sold, revenue, cost, profit) VALUES
-- Đơn hàng #1
(1, 1, 'Laptop Dell XPS 13', 1, 1500000, 1200000, 300000),

-- Đơn hàng #2
(2, 2, 'iPhone 15 Pro', 1, 2000000, 1600000, 400000),
(2, 3, 'AirPods Pro', 1, 500000, 400000, 100000),

-- Đơn hàng #3
(3, 4, 'Samsung Galaxy S24', 1, 800000, 650000, 150000);

-- ============================================
-- Kiểm tra dữ liệu
-- ============================================
SELECT 'Reporting database created successfully!' as message;
SELECT COUNT(*) as total_order_reports FROM orders_reports;
SELECT COUNT(*) as total_product_reports FROM product_reports;

-- Xem dữ liệu
SELECT * FROM orders_reports;
SELECT * FROM product_reports;