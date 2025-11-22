from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from .models import OrderReport, ProductReport
from .serializers import (
    OrderReportSerializer,
    ProductReportSerializer,
    CreateOrderReportSerializer,
    CreateProductReportSerializer
)
from .services import OrderService, ProductService, ReportCalculator

# =============== ORDER REPORTS VIEWS ===============

@api_view(['GET'])
def order_reports_list(request):
    """GET /reports/orders/ - Lấy danh sách tất cả báo cáo đơn hàng"""
    reports = OrderReport.objects.all()
    serializer = OrderReportSerializer(reports, many=True)
    return Response({
        'success': True,
        'count': len(serializer.data),
        'data': serializer.data
    })


@api_view(['GET'])
def order_report_detail(request, pk):
    """GET /reports/orders/<id>/ - Lấy chi tiết báo cáo đơn hàng"""
    try:
        report = OrderReport.objects.get(pk=pk)
    except OrderReport.DoesNotExist:
        return Response(
            {
                'success': False,
                'error': 'Không tìm thấy báo cáo đơn hàng'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = OrderReportSerializer(report)
    return Response({
        'success': True,
        'data': serializer.data
    })


@api_view(['POST'])
def order_report_create(request):
    """POST /reports/orders/ - Tạo báo cáo đơn hàng mới"""
    serializer = CreateOrderReportSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    order_id = serializer.validated_data['order_id']
    
    # Kiểm tra xem đã có báo cáo cho order này chưa
    existing_report = OrderReport.objects.filter(order_id=order_id).first()
    if existing_report:
        return Response({
            'success': False,
            'error': f'Báo cáo cho đơn hàng #{order_id} đã tồn tại',
            'existing_report_id': existing_report.id
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Lấy thông tin đơn hàng từ Orders Service
    order_data = OrderService.get_order(order_id)
    
    if not order_data:
        return Response({
            'success': False,
            'error': f'Không tìm thấy đơn hàng #{order_id} trong Orders Service'
        }, status=status.HTTP_404_NOT_FOUND)
    
    try:
        # Tính toán báo cáo
        total_revenue, total_cost, total_profit, product_reports_data = \
            ReportCalculator.calculate_order_report(order_data)
        
        with transaction.atomic():
            # Tạo order report
            order_report = OrderReport.objects.create(
                order_id=order_id,
                total_revenue=total_revenue,
                total_cost=total_cost,
                total_profit=total_profit
            )
            
            # Tạo product reports
            for product_data in product_reports_data:
                ProductReport.objects.create(
                    order_report=order_report,
                    **product_data
                )
            
            serializer = OrderReportSerializer(order_report)
            return Response({
                'success': True,
                'message': f'Tạo báo cáo cho đơn hàng #{order_id} thành công',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({
            'success': False,
            'error': 'Tạo báo cáo thất bại',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def order_report_delete(request, pk):
    """DELETE /reports/orders/<id>/ - Xóa báo cáo đơn hàng"""
    try:
        report = OrderReport.objects.get(pk=pk)
    except OrderReport.DoesNotExist:
        return Response(
            {
                'success': False,
                'error': 'Không tìm thấy báo cáo đơn hàng'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    report_id = report.id
    order_id = report.order_id
    report.delete()
    
    return Response({
        'success': True,
        'message': f'Đã xóa báo cáo #{report_id} cho đơn hàng #{order_id}'
    }, status=status.HTTP_200_OK)


# =============== PRODUCT REPORTS VIEWS ===============

@api_view(['GET'])
def product_reports_list(request):
    """GET /reports/products/ - Lấy danh sách tất cả báo cáo sản phẩm"""
    reports = ProductReport.objects.all()
    serializer = ProductReportSerializer(reports, many=True)
    return Response({
        'success': True,
        'count': len(serializer.data),
        'data': serializer.data
    })


@api_view(['GET'])
def product_report_detail(request, pk):
    """GET /reports/products/<id>/ - Lấy chi tiết báo cáo sản phẩm"""
    try:
        report = ProductReport.objects.get(pk=pk)
    except ProductReport.DoesNotExist:
        return Response(
            {
                'success': False,
                'error': 'Không tìm thấy báo cáo sản phẩm'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = ProductReportSerializer(report)
    return Response({
        'success': True,
        'data': serializer.data
    })


@api_view(['POST'])
def product_report_create(request):
    """
    POST /reports/products/ - Tạo báo cáo sản phẩm
    Tổng hợp từ tất cả đơn hàng có chứa sản phẩm này
    """
    serializer = CreateProductReportSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    product_id = serializer.validated_data['product_id']
    start_date = serializer.validated_data.get('start_date')
    end_date = serializer.validated_data.get('end_date')
    
    try:
        # Tính toán báo cáo sản phẩm
        report_data = ReportCalculator.calculate_product_report(
            product_id, start_date, end_date
        )
        
        if not report_data:
            return Response({
                'success': False,
                'error': f'Không tìm thấy sản phẩm #{product_id} hoặc không có dữ liệu'
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'success': True,
            'message': f'Báo cáo sản phẩm #{product_id} được tạo thành công',
            'data': report_data
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'success': False,
            'error': 'Tạo báo cáo sản phẩm thất bại',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def product_report_delete(request, pk):
    """DELETE /reports/products/<id>/ - Xóa báo cáo sản phẩm"""
    try:
        report = ProductReport.objects.get(pk=pk)
    except ProductReport.DoesNotExist:
        return Response(
            {
                'success': False,
                'error': 'Không tìm thấy báo cáo sản phẩm'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    report_id = report.id
    product_id = report.product_id
    report.delete()
    
    return Response({
        'success': True,
        'message': f'Đã xóa báo cáo sản phẩm #{report_id} (Product #{product_id})'
    }, status=status.HTTP_200_OK)


# =============== STATISTICS VIEWS (Bonus) ===============

@api_view(['GET'])
def reports_statistics(request):
    """GET /reports/statistics/ - Thống kê tổng quan"""
    from django.db.models import Sum, Count, Avg
    
    # Thống kê order reports
    order_stats = OrderReport.objects.aggregate(
        total_orders=Count('id'),
        total_revenue=Sum('total_revenue'),
        total_cost=Sum('total_cost'),
        total_profit=Sum('total_profit'),
        avg_revenue=Avg('total_revenue')
    )
    
    # Thống kê product reports
    product_stats = ProductReport.objects.aggregate(
        total_products=Count('id'),
        total_sold=Sum('total_sold'),
        total_revenue=Sum('revenue'),
        total_profit=Sum('profit')
    )
    
    return Response({
        'success': True,
        'data': {
            'order_statistics': order_stats,
            'product_statistics': product_stats
        }
    })