import apiClient from "../client";

export interface Proyecto {
  id: number;
  nombre: string;
  ubicacion: string;
  departamento: string;
  municipio: string;
  descripcion: string;
  coordenadas_lat: number | null;
  coordenadas_lng: number | null;
  area_total: number | null;
  is_active: boolean;
  total_lotes: number;
  lotes_disponibles: number;
  lotes_vendidos: number;
  created_at: string;
  updated_at: string;
}

export interface Lote {
  id: number;
  proyecto: number;
  proyecto_nombre: string;
  numero: string;
  manzana: string;
  medida_frente: number;
  medida_fondo: number;
  area_total: number;
  num_finca: string;
  folio: string;
  libro: string;
  precio_base: number;
  estado: "disponible" | "reservado" | "vendido";
  coordenadas_lat: number | null;
  coordenadas_lng: number | null;
  notas: string;
  fotografias: Fotografia[];
  created_at: string;
  updated_at: string;
}

export interface Fotografia {
  id: number;
  imagen: string;
  descripcion: string;
  orden: number;
  uploaded_at: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export const terrenosApi = {
  listProyectos: (params?: Record<string, string>) =>
    apiClient.get<PaginatedResponse<Proyecto>>("/terrenos/proyectos/", { params }),

  getProyecto: (id: number) =>
    apiClient.get<Proyecto>(`/terrenos/proyectos/${id}/`),

  createProyecto: (data: Partial<Proyecto>) =>
    apiClient.post<Proyecto>("/terrenos/proyectos/", data),

  updateProyecto: (id: number, data: Partial<Proyecto>) =>
    apiClient.put<Proyecto>(`/terrenos/proyectos/${id}/`, data),

  listLotes: (params?: Record<string, string>) =>
    apiClient.get<PaginatedResponse<Lote>>("/terrenos/lotes/", { params }),

  getLote: (id: number) =>
    apiClient.get<Lote>(`/terrenos/lotes/${id}/`),

  createLote: (data: Partial<Lote>) =>
    apiClient.post<Lote>("/terrenos/lotes/", data),

  updateLote: (id: number, data: Partial<Lote>) =>
    apiClient.patch<Lote>(`/terrenos/lotes/${id}/`, data),

  checkDisponibilidad: (id: number) =>
    apiClient.get(`/terrenos/lotes/${id}/disponibilidad/`),
};
