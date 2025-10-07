from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()
# Đường dẫn sẽ là /products (ví dụ: GET /products, POST /products)
router.register(r'products', ProductViewSet)
urlpatterns = router.urls