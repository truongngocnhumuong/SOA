# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# class HelloAPIView(APIView):
#     def get(self, request):
#         return Response({"message": "Hello World!"}, status=status.HTTP_200_OK)
from django.http import HttpResponse

def hello_world_view(request):
    return HttpResponse("Hello World!")