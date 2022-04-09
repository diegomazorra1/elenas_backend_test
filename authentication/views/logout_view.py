from django.contrib.auth import authenticate, login, logout
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView


class LogoutView(APIView):
    def post(self, request):
        logout(request)

        return Response({'status': 'Logout'}, status=status.HTTP_200_OK)
