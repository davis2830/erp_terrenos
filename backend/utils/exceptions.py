from rest_framework.exceptions import APIException


class LoteNoDisponibleError(APIException):
    status_code = 409
    default_detail = "El lote seleccionado no está disponible."
    default_code = "lote_no_disponible"


class ReservaExpiradaError(APIException):
    status_code = 410
    default_detail = "La reserva ha expirado."
    default_code = "reserva_expirada"


class SaldoInsuficienteError(APIException):
    status_code = 400
    default_detail = "El monto del abono excede el saldo pendiente."
    default_code = "saldo_insuficiente"


class FELError(APIException):
    status_code = 502
    default_detail = "Error al comunicarse con el servicio de Facturación Electrónica."
    default_code = "fel_error"
