#gọi API products
import requests
from django.conf import settings

class ProductService:
    """Service để giao tiếp với Product Management Service"""
    
    @staticmethod
    def get_product(product_id):
        """Lấy thông tin sản phẩm từ Product Service"""
        try:
            url = f"{settings.PRODUCT_SERVICE_URL}/products/{product_id}/"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException as e:
            print(f"Lỗi khi gọi Product Service: {e}")
            return None
    
    @staticmethod
    def check_stock(product_id, quantity):
        """
        Kiểm tra tồn kho sản phẩm
        Returns: (is_available: bool, result: dict/str)
        """
        product = ProductService.get_product(product_id)
        
        if not product:
            return False, f"Không tìm thấy sản phẩm ID: {product_id}"
        
        # Kiểm tra có thông tin stock không
        if 'stock_quantity' in product:
            available_quantity = product['stock_quantity']
        elif 'stock' in product:
            available_quantity = product['stock']
        else:
            # Nếu không có thông tin stock, coi như còn hàng
            print(f" Sản phẩm {product_id} không có thông tin stock, bỏ qua kiểm tra")
            return True, product
        
        if available_quantity < quantity:
            return False, f"Không đủ hàng. Còn lại: {available_quantity}, Yêu cầu: {quantity}"
        
        return True, product
    
    @staticmethod
    def update_stock(product_id, quantity, operation='decrease'):
        """
        Cập nhật tồn kho sản phẩm (tăng hoặc giảm)
        operation: 'decrease' (giảm) hoặc 'increase' (tăng)
        """
        try:
            # Tùy thuộc vào API của products service
            # Nếu có endpoint riêng để update stock
            url = f"{settings.PRODUCT_SERVICE_URL}/products/{product_id}/update-stock/"
            
            data = {
                'quantity': quantity,
                'operation': operation
            }
            
            response = requests.patch(url, json=data, timeout=5)
            
            if response.status_code in [200, 204]:
                print(f" Đã {operation} stock cho product {product_id}: {quantity}")
                return True, response.json() if response.content else {}
            
            print(f" Không thể cập nhật stock: {response.status_code}")
            return False, "Không thể cập nhật tồn kho"
            
        except requests.RequestException as e:
            print(f" Lỗi khi cập nhật stock: {e}")
            # Không return False để không làm gián đoạn flow
            # Vì việc cập nhật stock có thể xử lý sau
            return True, f"Cảnh báo: {str(e)}"

