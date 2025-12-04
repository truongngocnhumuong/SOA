from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Sum, Count
import json
import requests
from .models import OrderReport, ProductReport
from django.utils import timezone


def home(request):
    """Trang chủ Reports Service"""
    # Thống kê tổng quan
    total_orders = OrderReport.objects.count()
    total_revenue = OrderReport.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    total_products = ProductReport.objects.count()
    total_profit = sum(p.profit for p in ProductReport.objects.all())
    
    # Báo cáo đơn hàng gần đây
    recent_orders = OrderReport.objects.all()[:10]
    
    # Báo cáo sản phẩm bán chạy
    top_products = ProductReport.objects.order_by('-total_sold')[:10]
    
    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'total_profit': total_profit,
        'recent_orders': recent_orders,
        'top_products': top_products,
    }
    
    return render(request, 'reports/home.html', context)

# ==================== ORDER REPORTS ====================

@csrf_exempt
@require_http_methods(["POST"])
def create_order_report(request):
    """API: POST /api/reports/orders - Tạo báo cáo đơn hàng"""
    try:
        data = json.loads(request.body)
        
        # Lấy thông tin đơn hàng từ Orders Service
        try:
            order_response = requests.get(
                f'http://localhost:8002/api/orders/{data["order_id"]}/',
                timeout=5
            )
            
            if order_response.status_code == 200:
                order_data = order_response.json()
                
                report = OrderReport.objects.create(
                    order_id=data['order_id'],
                    customer_name=order_data.get('customer_name', ''),
                    total_amount=order_data.get('total_amount', data.get('total_amount', 0)),
                    order_date=order_data.get('created_at', None),
                    status=data.get('status', order_data.get('status', 'completed'))
                )
            else:
                # Nếu không lấy được từ Orders Service, dùng data từ request
                report = OrderReport.objects.create(
                    order_id=data['order_id'],
                    customer_name=data.get('customer_name', ''),
                    total_amount=data['total_amount'],
                    order_date=data.get('order_date'),
                    status=data.get('status', 'completed')
                )
        except requests.exceptions.RequestException:
            # Fallback nếu không kết nối được Orders Service
            report = OrderReport.objects.create(
                order_id=data['order_id'],
                customer_name=data.get('customer_name', ''),
                total_amount=data['total_amount'],
                order_date=data.get('order_date'),
                status=data.get('status', 'completed')
            )
        
        return JsonResponse({
            'report_id': report.id,
            'order_id': report.order_id,
            'total_amount': float(report.total_amount),
            'message': 'Order report created successfully'
        }, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def get_order_reports(request):
    """API: GET /api/reports/orders - Lấy tất cả báo cáo đơn hàng"""
    reports = OrderReport.objects.all()
    reports_list = []
    
    for report in reports:
        reports_list.append({
            'id': report.id,
            'order_id': report.order_id,
            'customer_name': report.customer_name,
            'total_amount': float(report.total_amount),
            'order_date': report.order_date.isoformat() if report.order_date else None,
            'status': report.status,
            'created_at': report.created_at.isoformat()
        })
    
    return JsonResponse(reports_list, safe=False)

@require_http_methods(["GET"])
def get_order_report(request, id):
    """API: GET /api/reports/orders/<id> - Lấy báo cáo đơn hàng theo ID"""
    try:
        report = OrderReport.objects.get(id=id)
        return JsonResponse({
            'id': report.id,
            'order_id': report.order_id,
            'customer_name': report.customer_name,
            'total_amount': float(report.total_amount),
            'order_date': report.order_date.isoformat() if report.order_date else None,
            'status': report.status,
            'created_at': report.created_at.isoformat()
        })
    except OrderReport.DoesNotExist:
        return JsonResponse({'error': 'Report not found'}, status=404)

@require_http_methods(["GET"])
def get_order_stats(request):
    """API: GET /api/reports/orders/stats - Thống kê đơn hàng"""
    total_orders = OrderReport.objects.count()
    total_revenue = OrderReport.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    status_stats = OrderReport.objects.values('status').annotate(
        count=Count('id'),
        total=Sum('total_amount')
    )
    
    return JsonResponse({
        'total_orders': total_orders,
        'total_revenue': float(total_revenue),
        'by_status': list(status_stats)
    })

# ==================== PRODUCT REPORTS ====================

@csrf_exempt
@require_http_methods(["POST"])
def create_product_report(request):
    """API: POST /api/reports/products - Tạo báo cáo sản phẩm"""
    try:
        data = json.loads(request.body)
        
        # Lấy thông tin sản phẩm từ Products Service
        try:
            product_response = requests.get(
                f'http://localhost:8001/api/products/{data["product_id"]}/',
                timeout=5
            )
            
            if product_response.status_code == 200:
                product_data = product_response.json()
                
                report = ProductReport.objects.create(
                    product_id=data['product_id'],
                    product_name=product_data.get('name', ''),
                    total_sold=data['total_sold'],
                    revenue=data['revenue'],
                    cost=data.get('cost', product_data.get('cost', 0))
                )
            else:
                report = ProductReport.objects.create(
                    product_id=data['product_id'],
                    product_name=data.get('product_name', ''),
                    total_sold=data['total_sold'],
                    revenue=data['revenue'],
                    cost=data.get('cost', 0)
                )
        except requests.exceptions.RequestException:
            report = ProductReport.objects.create(
                product_id=data['product_id'],
                product_name=data.get('product_name', ''),
                total_sold=data['total_sold'],
                revenue=data['revenue'],
                cost=data.get('cost', 0)
            )
        
        return JsonResponse({
            'report_id': report.id,
            'product_id': report.product_id,
            'product_name': report.product_name,
            'profit': float(report.profit),
            'message': 'Product report created successfully'
        }, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def get_product_reports(request):
    """API: GET /api/reports/products - Lấy tất cả báo cáo sản phẩm"""
    reports = ProductReport.objects.all()
    reports_list = []
    
    for report in reports:
        reports_list.append({
            'id': report.id,
            'product_id': report.product_id,
            'product_name': report.product_name,
            'total_sold': report.total_sold,
            'revenue': float(report.revenue),
            'cost': float(report.cost),
            'profit': float(report.profit),
            'created_at': report.created_at.isoformat()
        })
    
    return JsonResponse(reports_list, safe=False)

@require_http_methods(["GET"])
def get_product_report(request, id):
    """API: GET /api/reports/products/<id> - Lấy báo cáo sản phẩm theo ID"""
    try:
        report = ProductReport.objects.get(id=id)
        return JsonResponse({
            'id': report.id,
            'product_id': report.product_id,
            'product_name': report.product_name,
            'total_sold': report.total_sold,
            'revenue': float(report.revenue),
            'cost': float(report.cost),
            'profit': float(report.profit),
            'created_at': report.created_at.isoformat()
        })
    except ProductReport.DoesNotExist:
        return JsonResponse({'error': 'Report not found'}, status=404)

@require_http_methods(["GET"])
def get_product_stats(request):
    """API: GET /api/reports/products/stats - Thống kê sản phẩm"""
    total_products = ProductReport.objects.count()
    total_sold = ProductReport.objects.aggregate(Sum('total_sold'))['total_sold__sum'] or 0
    total_revenue = ProductReport.objects.aggregate(Sum('revenue'))['revenue__sum'] or 0
    total_cost = ProductReport.objects.aggregate(Sum('cost'))['cost__sum'] or 0
    
    # Top sản phẩm bán chạy
    top_sellers = ProductReport.objects.order_by('-total_sold')[:5].values()
    
    return JsonResponse({
        'total_products': total_products,
        'total_sold': total_sold,
        'total_revenue': float(total_revenue),
        'total_cost': float(total_cost),
        'total_profit': float(total_revenue - total_cost),
        'top_sellers': list(top_sellers)
    })

@require_http_methods(["GET"])
def dashboard(request):
    """API: GET /api/reports/dashboard - Dashboard tổng quan"""
    # Order stats
    order_stats = get_order_stats(request)
    order_data = json.loads(order_stats.content)
    
    # Product stats
    product_stats = get_product_stats(request)
    product_data = json.loads(product_stats.content)
    
    return JsonResponse({
        'orders': order_data,
        'products': product_data,
        'timestamp': timezone.now().isoformat()
    })