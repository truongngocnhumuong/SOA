from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import requests
from .models import Order, OrderItem
from django.db import transaction

def home(request):
    """Trang chủ Orders Service"""
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'orders/home.html', {'orders': orders})

@csrf_exempt
@require_http_methods(["POST"])
def create_order(request):
    """API: POST /api/orders - Tạo đơn hàng mới"""
    try:
        data = json.loads(request.body)
        
        order = Order.objects.create(
            customer_name=data['customer_name'],
            customer_email=data['customer_email'],
            status='pending'
        )
        
        return JsonResponse({
            'order_id': order.id,
            'customer_name': order.customer_name,
            'status': order.status,
            'created_at': order.created_at.isoformat(),
            'message': 'Order created successfully'
        }, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def add_order_items(request):
    """API: POST /api/order_items - Thêm sản phẩm vào đơn hàng"""
    try:
        data = json.loads(request.body)
        order_id = data['order_id']
        items = data['items']
        
        order = Order.objects.get(id=order_id)
        
        with transaction.atomic():
            total = 0
            for item in items:
                # Lấy thông tin sản phẩm từ Products Service
                try:
                    product_response = requests.get(
                        f'http://localhost:8001/api/products/{item["product_id"]}/',
                        timeout=5
                    )
                    
                    if product_response.status_code == 200:
                        product = product_response.json()
                        
                        # Kiểm tra số lượng
                        if product['quantity'] < item['quantity']:
                            return JsonResponse({
                                'error': f'Không đủ số lượng cho sản phẩm {product["name"]}'
                            }, status=400)
                        
                        # Tạo order item
                        OrderItem.objects.create(
                            order=order,
                            product_id=item['product_id'],
                            product_name=product['name'],
                            quantity=item['quantity'],
                            unit_price=item.get('unit_price', product['price'])
                        )
                        
                        # Cập nhật số lượng sản phẩm
                        new_quantity = product['quantity'] - item['quantity']
                        requests.put(
                            f'http://localhost:8001/api/products/{item["product_id"]}/update/',
                            json={'quantity': new_quantity},
                            timeout=5
                        )
                        
                        total += item['quantity'] * item.get('unit_price', product['price'])
                except requests.exceptions.RequestException as e:
                    return JsonResponse({
                        'error': f'Không thể kết nối với Products Service: {str(e)}'
                    }, status=500)
            
            order.total_amount = total
            order.save()
        
        return JsonResponse({
            'order_id': order.id,
            'total_amount': float(order.total_amount),
            'items_count': len(items),
            'message': 'Order items added successfully'
        }, status=201)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["PUT"])
def update_order_status(request, id):
    """API: PUT /api/orders/<id> - Cập nhật trạng thái đơn hàng"""
    try:
        order = Order.objects.get(id=id)
        data = json.loads(request.body)
        
        if 'status' in data:
            order.status = data['status']
            order.save()
        
        return JsonResponse({
            'order_id': order.id,
            'status': order.status,
            'message': 'Order status updated successfully'
        })
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def get_orders(request):
    """API: GET /api/orders - Lấy danh sách đơn hàng"""
    orders = Order.objects.all().values()
    orders_list = []
    for order in orders:
        order_dict = dict(order)
        order_dict['total_amount'] = float(order_dict['total_amount'])
        order_dict['created_at'] = order_dict['created_at'].isoformat()
        order_dict['updated_at'] = order_dict['updated_at'].isoformat()
        orders_list.append(order_dict)
    return JsonResponse(orders_list, safe=False)

@require_http_methods(["GET"])
def get_order(request, id):
    """API: GET /api/orders/<id> - Lấy chi tiết đơn hàng"""
    try:
        order = Order.objects.get(id=id)
        items = OrderItem.objects.filter(order=order).values()
        
        return JsonResponse({
            'id': order.id,
            'customer_name': order.customer_name,
            'customer_email': order.customer_email,
            'status': order.status,
            'total_amount': float(order.total_amount),
            'items': list(items),
            'created_at': order.created_at.isoformat()
        })
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)