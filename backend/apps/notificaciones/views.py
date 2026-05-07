from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import NotificacionEnviada, PlantillaMensaje
from .serializers import (
    EnviarMensajeSerializer,
    NotificacionEnviadaSerializer,
    PlantillaMensajeSerializer,
)


class PlantillaMensajeListCreateView(generics.ListCreateAPIView):
    queryset = PlantillaMensaje.objects.all()
    serializer_class = PlantillaMensajeSerializer
    filterset_fields = ["tipo", "is_active"]


class PlantillaMensajeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlantillaMensaje.objects.all()
    serializer_class = PlantillaMensajeSerializer


class NotificacionListView(generics.ListAPIView):
    queryset = NotificacionEnviada.objects.select_related("cliente", "plantilla").all()
    serializer_class = NotificacionEnviadaSerializer
    filterset_fields = ["canal", "estado", "cliente"]
    ordering_fields = ["created_at"]


class EnviarMensajeView(APIView):
    """Envía un mensaje de WhatsApp/SMS a un cliente."""

    def post(self, request):
        serializer = EnviarMensajeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Placeholder: se implementará con TwilioWhatsAppService
        return Response(
            {"detail": "Endpoint pendiente de implementación."},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )
