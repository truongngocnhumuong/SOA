# from django.http import HttpResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# def hello_world_view(request):
#     return HttpResponse("Hello World!")

class HelloAuthAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_info = f"Hello {request.user.username}!" if request.user.is_authenticated else "Hello World!"

        return Response({
            "message": user_info,
            "note": "Token xac thuc thanh cong!"
        }, status=200)