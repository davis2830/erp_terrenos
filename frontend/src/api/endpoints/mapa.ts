import apiClient from "../client";

export interface CoordenadaLote {
  id: number;
  lote: number;
  lote_numero: string;
  lote_estado: "disponible" | "reservado" | "vendido";
  lote_precio: string;
  svg_path: string;
}

export interface MapaProyecto {
  id: number;
  proyecto: number;
  proyecto_nombre: string;
  svg_data: string;
  configuracion_colores: Record<string, string>;
  ancho: number;
  alto: number;
  coordenadas: CoordenadaLote[];
  created_at: string;
  updated_at: string;
}

export interface DashboardStats {
  lotes: {
    total: number;
    disponibles: number;
    reservados: number;
    vendidos: number;
  };
  valores: {
    total: number;
    vendido: number;
    disponible: number;
  };
  proyectos_activos: number;
}

export const mapaApi = {
  getMapa: (proyectoId: number) =>
    apiClient.get<MapaProyecto>(`/mapa/proyectos/${proyectoId}/mapa/`),
};

export const dashboardApi = {
  getStats: () =>
    apiClient.get<DashboardStats>("/terrenos/dashboard/stats/"),
};
