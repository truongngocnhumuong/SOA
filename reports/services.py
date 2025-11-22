import requests
from django.conf import settings
from decimal import Decimal

class OrderService:
    """Service để gọi Orders Service"""
    
    @staticmethod
    def get_order(order_id):
        """Lấy thông tin đơn hàng từ Orders Service"""
        try:
            url = f"{settings.ORDER_SERVICE_URL}/orders/{order_id}/"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('data') if 'data' in data else data
            return None
        except requests.RequestException as e:
            print(f"❌ Lỗi khi gọi Orders Service: {e}")
            return None
    
    @staticmethod
    def get_all_orders():
        """Lấy danh sách tất cả đơn hàng"""
        try:
            url = f"{settings.ORDER_SERVICE_URL}/orders/"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('data', []) if 'data' in data else data
            return []
        except requests.RequestException as e:
            print(f"❌ Lỗi khi gọi Orders Service: {e}")
            return []


class ProductService:
    """Service để gọi Products Service"""
    
    @staticmethod
    def get_product(product_id):
        """Lấy thông tin sản phẩm từ Products Service"""
        try:
            url = f"{settings.PRODUCT_SERVICE_URL}/products/{product_id}/"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('data') if 'data' in data else data
            return None
        except requests.RequestException as e:
            print(f"❌ Lỗi khi gọi Products Service: {e}")
            return None
    
    @staticmethod
    def get_all_products():
        """Lấy danh sách tất cả sản phẩm"""
        try:
            url = f"{settings.PRODUCT_SERVICE_URL}/products/"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('data', []) if 'data' in data else data
            return []
        except requests.RequestException as e:
            print(f"❌ Lỗi khi gọi Products Service: {e}")
            return []


class ReportCalculator:
    """Class để tính toán báo cáo"""
    
    @staticmethod
    def calculate_order_report(order_data):
        """
        Tính toán báo cáo cho một đơn hàng
        Returns: (total_revenue, total_cost, total_profit, product_reports_data)
        """
        total_revenue = Decimal('0')
        total_cost = Decimal('0')
        product_reports_data = []
        
        # Lấy order items từ order data
        order_items = order_data.get('order_items', [])
        
        for item in order_items:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 0)
            unit_price = Decimal(str(item.get('unit_price', 0)))
            
            # Lấy thông tin sản phẩm để biết cost
            product = ProductService.get_product(product_id)
            
            # Tính cost (giả sử cost = 80% của selling price)
            # Hoặc lấy từ product service nếu có trường 'cost'
            if product and 'cost' in product:
                unit_cost = Decimal(str(product['cost']))
            else:
                unit_cost = unit_price * Decimal('0.8')  # Giả định cost = 80% price
            
            # Tính toán
            item_revenue = unit_price * quantity
            item_cost = unit_cost * quantity
            item_profit = item_revenue - item_cost
            
            total_revenue += item_revenue
            total_cost += item_cost
            
            # Thêm vào danh sách product reports
            product_reports_data.append({
                'product_id': product_id,
                'product_name': item.get('product_name', ''),
                'total_sold': quantity,
                'revenue': item_revenue,
                'cost': item_cost,
                'profit': item_profit
            })
        
        total_profit = total_revenue - total_cost
        
        return total_revenue, total_cost, total_profit, product_reports_data
    
    @staticmethod
    def calculate_product_report(product_id, start_date=None, end_date=None):
        """
        Tính toán báo cáo cho một sản phẩm dựa trên tất cả đơn hàng
        """
        # Lấy tất cả đơn hàng
        orders = OrderService.get_all_orders()
        
        total_sold = 0
        total_revenue = Decimal('0')
        total_cost = Decimal('0')
        product_name = ''
        
        # Lấy thông tin sản phẩm
        product = ProductService.get_product(product_id)
        if product:
            product_name = product.get('name', '')
            unit_price = Decimal(str(product.get('price', 0)))
            unit_cost = Decimal(str(product.get('cost', unit_price * Decimal('0.8'))))
        else:
            return None
        
        # Duyệt qua tất cả đơn hàng
        for order in orders:
            order_items = order.get('order_items', [])
            
            for item in order_items:
                if item.get('product_id') == product_id:
                    quantity = item.get('quantity', 0)
                    total_sold += quantity
                    total_revenue += Decimal(str(item.get('unit_price', 0))) * quantity
                    total_cost += unit_cost * quantity
        
        total_profit = total_revenue - total_cost
        
        return {
            'product_id': product_id,
            'product_name': product_name,
            'total_sold': total_sold,
            'revenue': total_revenue,
            'cost': total_cost,
            'profit': total_profit
        }