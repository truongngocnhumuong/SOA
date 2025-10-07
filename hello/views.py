# from django.http import HttpResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# def hello_world_view(request):
#     return HttpResponse("Hello World!")
# Lớp API Hello World được bảo vệ
class HelloAuthAPIView(APIView):
    # 1. Thêm lớp xác thực JWT
    authentication_classes = [JWTAuthentication]
    # 2. Thêm lớp phân quyền: chỉ người dùng đã xác thực mới được truy cập
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Lấy thông tin user (đã được xác thực qua token)
        user_info = f"Hello {request.user.username}!" if request.user.is_authenticated else "Hello World!"

        return Response({
            "message": user_info,
            "note": "Token xac thuc thanh cong!"
        }, status=200)