from rest_framework import routers
from .views import BorrowViewSet

router = routers.DefaultRouter()
router.register(r'borrows', BorrowViewSet)

urlpatterns = router.urls