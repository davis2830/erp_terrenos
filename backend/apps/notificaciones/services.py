"""
Servicio de envío de mensajes vía Twilio (WhatsApp/SMS).
Se implementará en la fase de codificación.
"""

# TODO: Implementar TwilioWhatsAppService
# from django.conf import settings
# from twilio.rest import Client
#
# class TwilioWhatsAppService:
#     def __init__(self):
#         self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#         self.from_number = settings.TWILIO_WHATSAPP_FROM
#
#     def enviar_whatsapp(self, telefono_destino, mensaje):
#         """Envía un mensaje de WhatsApp."""
#         ...
#
#     def enviar_sms(self, telefono_destino, mensaje):
#         """Envía un SMS."""
#         ...
#
#     def renderizar_plantilla(self, plantilla, contexto):
#         """Reemplaza variables en la plantilla con datos del contexto."""
#         ...
