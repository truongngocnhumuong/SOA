from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from .models import Order, OrderItem
from .serializers import (
    OrderSerializer, 
    OrderItemSerializer, 
    CreateOrderSerializer
)
from .services import ProductService

# =============== ORDER VIEWS ===============

@api_view(['GET'])
def order_list(request):
    """GET /orders/ - Lấy danh sách tất cả đơn hàng"""
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response({
        'success': True,
        'count': len(serializer.data),
        'data': serializer.data
    })


@api_view(['GET'])
def order_detail(request, pk):
    """GET /orders/<id>/ - Lấy chi tiết một đơn hàng"""
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(
            {
                'success': False,
                'error': 'Không tìm thấy đơn hàng'
            }, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = OrderSerializer(order)
    return Response({
        'success': True,
        'data': serializer.data
    })


@api_view(['POST'])
def order_create(request):
    """POST /orders/ - Tạo đơn hàng mới"""
    serializer = CreateOrderSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    validated_data = serializer.validated_data
    items_data = validated_data['items']
    
    # Bước 1: Kiểm tra tồn kho cho tất cả sản phẩm
    products_info = []
    for item in items_data:
        is_available, result = ProductService.check_stock(
            item['product_id'], 
            item['quantity']
        )
        
        if not is_available:
            return Response(
                {
                    'success': False,
                    'error': 'Kiểm tra tồn kho thất bại',
                    'message': result,
                    'product_id': item['product_id']
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        products_info.append(result)
    
    # Bước 2: Tạo đơn hàng và order items trong transaction
    try:
        with transaction.atomic():
            # Tạo order
            order = Order.objects.create(
                customer_name=validated_data['customer_name'],
                customer_email=validated_data['customer_email'],
                status='pending'
            )
            
            # Tạo order items
            for i, item_data in enumerate(items_data):
                product = products_info[i]
                
                # Lấy giá và tên từ product info
                product_name = product.get('name', f"Product {item_data['product_id']}")
                product_price = product.get('price', 0)
                
                OrderItem.objects.create(
                    order=order,
                    product_id=item_data['product_id'],
                    product_name=product_name,
                    quantity=item_data['quantity'],
                    unit_price=product_price
                )
                
                # Cập nhật tồn kho (giảm số lượng)
                ProductService.update_stock(
                    item_data['product_id'],
                    item_data['quantity'],
                    'decrease'
                )
            
            # Tính tổng tiền
            order.calculate_total()
            
            serializer = OrderSerializer(order)
            return Response({
                'success': True,
                'message': 'Tạo đơn hàng thành công',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        return Response(
            {
                'success': False,
                'error': 'Tạo đơn hàng thất bại', 
                'message': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT'])
def order_update(request, pk):
    """PUT /orders/<id>/ - Cập nhật trạng thái đơn hàng"""
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(
            {
                'success': False,
                'error': 'Không tìm thấy đơn hàng'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    new_status = request.data.get('status')
    
    if not new_status:
        return Response(
            {
                'success': False,
                'error': 'Thiếu trường status'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    valid_statuses = ['pending', 'completed', 'cancelled']
    if new_status not in valid_statuses:
        return Response(
            {
                'success': False,
                'error': f'Status không hợp lệ. Phải là một trong: {", ".join(valid_statuses)}'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Nếu đơn hàng bị hủy, hoàn lại tồn kho
    if new_status == 'cancelled' and order.status != 'cancelled':
        for item in order.order_items.all():
            ProductService.update_stock(
                item.product_id,
                item.quantity,
                'increase'
            )
    
    old_status = order.status
    order.status = new_status
    order.save()
    
    serializer = OrderSerializer(order)
    return Response({
        'success': True,
        'message': f'Cập nhật trạng thái từ {old_status} sang {new_status}',
        'data': serializer.data
    })


@api_view(['DELETE'])
def order_delete(request, pk):
    """DELETE /orders/<id>/ - Xóa đơn hàng"""
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(
            {
                'success': False,
                'error': 'Không tìm thấy đơn hàng'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Hoàn lại tồn kho nếu đơn hàng chưa bị hủy
    if order.status != 'cancelled':
        for item in order.order_items.all():
            ProductService.update_stock(
                item.product_id,
                item.quantity,
                'increase'
            )
    
    order_id = order.id
    order.delete()
    
    return Response(
        {
            'success': True,
            'message': f'Đã xóa đơn hàng #{order_id}'
        },
        status=status.HTTP_200_OK
    )


# =============== ORDER ITEM VIEWS ===============

@api_view(['GET'])
def order_item_list(request):
    """GET /order_items/ - Lấy danh sách tất cả mặt hàng"""
    items = OrderItem.objects.all()
    serializer = OrderItemSerializer(items, many=True)
    return Response({
        'success': True,
        'count': len(serializer.data),
        'data': serializer.data
    })


@api_view(['GET'])
def order_item_detail(request, pk):
    """GET /order_items/<id>/ - Lấy chi tiết một mặt hàng"""
    try:
        item = OrderItem.objects.get(pk=pk)
    except OrderItem.DoesNotExist:
        return Response(
            {
                'success': False,
                'error': 'Không tìm thấy mặt hàng'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = OrderItemSerializer(item)
    return Response({
        'success': True,
        'data': serializer.data
    })


@api_view(['POST'])
def order_item_create(request):
    """POST /order_items/ - Tạo mặt hàng mới"""
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity')
    order_id = request.data.get('order')
    
    if not all([product_id, quantity, order_id]):
        return Response(
            {
                'success': False,
                'error': 'Thiếu thông tin: product_id, quantity, và order'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Kiểm tra order có tồn tại không
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response(
            {
                'success': False,
                'error': f'Không tìm thấy đơn hàng ID: {order_id}'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Kiểm tra tồn kho
    is_available, result = ProductService.check_stock(product_id, quantity)
    
    if not is_available:
        return Response(
            {
                'success': False,
                'error': 'Kiểm tra tồn kho thất bại', 
                'message': result
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Tạo order item
    try:
        item = OrderItem.objects.create(
            order=order,
            product_id=product_id,
            product_name=result.get('name', f'Product {product_id}'),
            quantity=quantity,
            unit_price=result.get('price', 0)
        )
        
        # Cập nhật tồn kho
        ProductService.update_stock(product_id, quantity, 'decrease')
        
        serializer = OrderItemSerializer(item)
        return Response({
            'success': True,
            'message': 'Thêm sản phẩm vào đơn hàng thành công',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {
                'success': False,
                'error': 'Tạo mặt hàng thất bại', 
                'message': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT'])
def order_item_update(request, pk):
    """PUT /order_items/<id>/ - Cập nhật mặt hàng"""
    try:
        item = OrderItem.objects.get(pk=pk)
    except OrderItem.DoesNotExist:
        return Response(
            {
                'success': False,
                'error': 'Không tìm thấy mặt hàng'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    new_quantity = request.data.get('quantity')
    
    if not new_quantity:
        return Response(
            {
                'success': False,
                'error': 'Thiếu trường quantity'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        new_quantity = int(new_quantity)
    except ValueError:
        return Response(
            {
                'success': False,
                'error': 'quantity phải là số nguyên'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Tính chênh lệch số lượng
    quantity_diff = new_quantity - item.quantity
    
    if quantity_diff > 0:
        # Cần thêm sản phẩm, kiểm tra tồn kho
        is_available, result = ProductService.check_stock(item.product_id, quantity_diff)
        if not is_available:
            return Response(
                {
                    'success': False,
                    'error': 'Không đủ hàng', 
                    'message': result
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        ProductService.update_stock(item.product_id, quantity_diff, 'decrease')
    elif quantity_diff < 0:
        # Giảm số lượng, hoàn lại tồn kho
        ProductService.update_stock(item.product_id, abs(quantity_diff), 'increase')
    
    item.quantity = new_quantity
    item.save()
    
    serializer = OrderItemSerializer(item)
    return Response({
        'success': True,
        'message': f'Cập nhật số lượng thành công',
        'data': serializer.data
    })


@api_view(['DELETE'])
def order_item_delete(request, pk):
    """DELETE /order_items/<id>/ - Xóa mặt hàng"""
    try:
        item = OrderItem.objects.get(pk=pk)
    except OrderItem.DoesNotExist:
        return Response(
            {
                'success': False,
                'error': 'Không tìm thấy mặt hàng'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Hoàn lại tồn kho
    ProductService.update_stock(item.product_id, item.quantity, 'increase')
    
    order = item.order
    item_id = item.id
    item.delete()
    
    # Cập nhật lại tổng tiền của đơn hàng
    order.calculate_total()
    
    return Response(
        {
            'success': True,
            'message': f'Đã xóa mặt hàng #{item_id}'
        },
        status=status.HTTP_200_OK
    )