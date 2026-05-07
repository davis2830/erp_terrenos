from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .permissions import IsAdminOrGerente
from .serializers import (
    CustomTokenObtainPairSerializer,
    ProfileSerializer,
    UserCreateSerializer,
    UserSerializer,
)

User = get_user_model()


class LoginView(TokenObtainPairView):
    """Endpoint de login. Retorna tokens JWT + datos del usuario."""

    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]


class TokenRefreshApiView(TokenRefreshView):
    """Endpoint para refrescar el token JWT."""

    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    """Obtener y actualizar el perfil del usuario autenticado."""

    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user


class UserListCreateView(generics.ListCreateAPIView):
    """Listar y crear usuarios (solo admin/gerente)."""

    queryset = User.objects.all()
    permission_classes = [IsAdminOrGerente]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserCreateSerializer
        return UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de usuario."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrGerente]


class LogoutView(APIView):
    """Endpoint de logout (invalidación del token en el cliente)."""

    def post(self, request):
        return Response(
            {"detail": "Sesión cerrada exitosamente."},
            status=status.HTTP_200_OK,
        )
