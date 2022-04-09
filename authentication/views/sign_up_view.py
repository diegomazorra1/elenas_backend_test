from rest_framework import status, generics

from authentication.serializers import UserSerializer


class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer
