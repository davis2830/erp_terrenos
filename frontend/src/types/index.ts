export type UserRole = "admin" | "gerente" | "vendedor";

export type EstadoLote = "disponible" | "reservado" | "vendido";

export type EstadoReserva = "activa" | "concretada" | "expirada" | "cancelada";

export type EstadoVenta = "activa" | "completada" | "cancelada";

export type EstadoCuota = "pendiente" | "pagada" | "mora" | "parcial";

export type MetodoPago = "efectivo" | "transferencia" | "cheque" | "deposito" | "otro";

export type TipoDocumento = "dpi" | "rtu" | "promesa_cv" | "escritura" | "otro";

export type CanalNotificacion = "whatsapp" | "sms";

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export const ESTADO_LOTE_COLORS: Record<EstadoLote, string> = {
  disponible: "#22c55e",
  reservado: "#f59e0b",
  vendido: "#ef4444",
};

export const ESTADO_LOTE_LABELS: Record<EstadoLote, string> = {
  disponible: "Disponible",
  reservado: "Reservado",
  vendido: "Vendido",
};
