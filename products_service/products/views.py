from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Product

def home(request):
    """Trang chủ Products Service"""
    products = Product.objects.all()
    return render(request, 'products/home.html', {'products': products})

@require_http_methods(["GET"])
def get_products(request):
    """API: GET /api/products - Lấy danh sách sản phẩm"""
    products = Product.objects.all().values()
    return JsonResponse(list(products), safe=False)

@require_http_methods(["GET"])
def get_product(request, id):
    """API: GET /api/products/<id> - Lấy thông tin 1 sản phẩm"""
    try:
        product = Product.objects.get(id=id)
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'quantity': product.quantity,
            'cost': float(product.cost),
            'description': product.description,
        })
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

@csrf_exempt
@require_http_methods(["PUT"])
def update_product(request, id):
    """API: PUT /api/products/<id> - Cập nhật sản phẩm"""
    try:
        product = Product.objects.get(id=id)
        data = json.loads(request.body)
        
        if 'quantity' in data:
            product.quantity = data['quantity']
        if 'price' in data:
            product.price = data['price']
        if 'name' in data:
            product.name = data['name']
            
        product.save()
        
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'price': float(product.price),
            'message': 'Product updated successfully'
        })
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)