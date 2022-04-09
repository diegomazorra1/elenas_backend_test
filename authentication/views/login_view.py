from django.contrib.auth import authenticate, login, logout
from rest_framework import status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created

from authentication.serializers import UserSerializer


class LoginView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return Response({'status': 'Success'},
                            status=status.HTTP_200_OK)

        return Response(
            status=status.HTTP_404_NOT_FOUND)





@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # Aquí deberíamos mandar un correo al cliente...
    print(
        f"\nRecupera la contraseña del correo '{reset_password_token.user.email}' usando el token '{reset_password_token.key}' desde la API http://localhost:8000/api/auth/reset/confirm/.\n\n "

        f"También puedes hacerlo directamente desde el cliente web en http://localhost:3000/new-password/?token={reset_password_token.key}.\n")
