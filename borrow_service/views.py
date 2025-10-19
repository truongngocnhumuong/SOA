from rest_framework import viewsets
from .models import Borrow
from .serializers import BorrowSerializer

class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
