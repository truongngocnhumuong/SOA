from django.urls import path
# from .views import hello_world_view
from .views import HelloAuthAPIView

urlpatterns = [
    # path('hello/', hello_world_view, name='hello_world'),
    path('auth/', HelloAuthAPIView.as_view(), name='hello_auth'),
]