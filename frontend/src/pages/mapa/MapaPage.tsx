import { useEffect, useState } from "react";
import { ZoomIn, ZoomOut, RotateCcw } from "lucide-react";
import MainLayout from "../../components/layout/MainLayout";
import { mapaApi, type MapaProyecto, type CoordenadaLote } from "../../api/endpoints/mapa";
import { terrenosApi, type Proyecto } from "../../api/endpoints/terrenos";
import { ESTADO_LOTE_COLORS, ESTADO_LOTE_LABELS } from "../../types";

function formatQ(value: string | number): string {
  const n = typeof value === "string" ? parseFloat(value) : value;
  return `Q ${n.toLocaleString("es-GT", { minimumFractionDigits: 2 })}`;
}

export default function MapaPage() {
  const [mapa, setMapa] = useState<MapaProyecto | null>(null);
  const [proyectos, setProyectos] = useState<Proyecto[]>([]);
  const [selectedProyecto, setSelectedProyecto] = useState<number | null>(null);
  const [hoveredLote, setHoveredLote] = useState<CoordenadaLote | null>(null);
  const [selectedLote, setSelectedLote] = useState<CoordenadaLote | null>(null);
  const [zoom, setZoom] = useState(1);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    terrenosApi.listProyectos()
      .then((res) => {
        setProyectos(res.data.results);
        if (res.data.results.length > 0) {
          setSelectedProyecto(res.data.results[0].id);
        }
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (!selectedProyecto) return;
    setLoading(true);
    mapaApi.getMapa(selectedProyecto)
      .then((res) => setMapa(res.data))
      .catch(() => setMapa(null))
      .finally(() => setLoading(false));
  }, [selectedProyecto]);

  const colors = mapa?.configuracion_colores || ESTADO_LOTE_COLORS;

  const manzanas: Record<string, CoordenadaLote[]> = {};
  mapa?.coordenadas.forEach((c) => {
    const mz = c.lote_numero.split("-")[0];
    if (!manzanas[mz]) manzanas[mz] = [];
    manzanas[mz].push(c);
  });

  const activeLote = selectedLote || hoveredLote;

  return (
    <MainLayout title="Mapa Interactivo">
      <div className="flex gap-6">
        <div className="flex-1 bg-white rounded-xl shadow-sm border border-gray-100">
          <div className="p-4 border-b border-gray-100 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <select
                value={selectedProyecto || ""}
                onChange={(e) => setSelectedProyecto(Number(e.target.value))}
                className="border border-gray-300 rounded-lg px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-emerald-500"
              >
                {proyectos.map((p) => (
                  <option key={p.id} value={p.id}>{p.nombre}</option>
                ))}
              </select>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setZoom((z) => Math.min(z + 0.2, 2))}
                className="p-2 hover:bg-gray-100 rounded-lg"
                title="Acercar"
              >
                <ZoomIn size={18} />
              </button>
              <button
                onClick={() => setZoom((z) => Math.max(z - 0.2, 0.5))}
                className="p-2 hover:bg-gray-100 rounded-lg"
                title="Alejar"
              >
                <ZoomOut size={18} />
              </button>
              <button
                onClick={() => { setZoom(1); setSelectedLote(null); }}
                className="p-2 hover:bg-gray-100 rounded-lg"
                title="Restablecer"
              >
                <RotateCcw size={18} />
              </button>
              <span className="text-xs text-gray-400 ml-2">{Math.round(zoom * 100)}%</span>
            </div>
          </div>

          {loading ? (
            <div className="flex items-center justify-center h-96">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-600" />
            </div>
          ) : mapa ? (
            <div className="p-4 overflow-auto">
              <svg
                viewBox={`0 0 ${mapa.ancho} ${mapa.alto}`}
                width={mapa.ancho * zoom}
                height={mapa.alto * zoom}
                className="mx-auto"
              >
                {Object.entries(manzanas).map(([mz, coords]) => {
                  const points = coords.map((c) => {
                    const pts = c.svg_path.split(" ").map((p) => p.split(",").map(Number));
                    return { coord: c, pts };
                  });
                  const allX = points.flatMap((p) => p.pts.map((pt) => pt[0]));
                  const allY = points.flatMap((p) => p.pts.map((pt) => pt[1]));
                  const minX = Math.min(...allX);
                  const minY = Math.min(...allY);
                  const maxX = Math.max(...allX);

                  return (
                    <g key={mz}>
                      <text
                        x={(minX + maxX) / 2}
                        y={minY - 8}
                        textAnchor="middle"
                        className="text-xs font-bold"
                        fill="#374151"
                        fontSize="14"
                      >
                        Manzana {mz}
                      </text>
                      {points.map(({ coord, pts }) => {
                        const isActive = activeLote?.id === coord.id;
                        const color = colors[coord.lote_estado] || "#9ca3af";
                        return (
                          <g key={coord.id}>
                            <polygon
                              points={pts.map((p) => p.join(",")).join(" ")}
                              fill={color}
                              stroke={isActive ? "#1e293b" : "#ffffff"}
                              strokeWidth={isActive ? 2.5 : 1}
                              opacity={isActive ? 1 : 0.85}
                              className="cursor-pointer transition-all"
                              onMouseEnter={() => setHoveredLote(coord)}
                              onMouseLeave={() => setHoveredLote(null)}
                              onClick={() => setSelectedLote(coord)}
                            />
                            <text
                              x={(pts[0][0] + pts[2][0]) / 2}
                              y={(pts[0][1] + pts[2][1]) / 2 + 1}
                              textAnchor="middle"
                              dominantBaseline="middle"
                              fill="white"
                              fontSize="10"
                              fontWeight="bold"
                              className="pointer-events-none select-none"
                            >
                              {coord.lote_numero.split("-")[1]}
                            </text>
                          </g>
                        );
                      })}
                    </g>
                  );
                })}
              </svg>

              <div className="flex items-center justify-center gap-6 mt-4 text-sm">
                {(["disponible", "reservado", "vendido"] as const).map((estado) => (
                  <div key={estado} className="flex items-center gap-2">
                    <div
                      className="w-4 h-4 rounded"
                      style={{ backgroundColor: colors[estado] || ESTADO_LOTE_COLORS[estado] }}
                    />
                    <span className="text-gray-600">{ESTADO_LOTE_LABELS[estado]}</span>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-center h-96 text-gray-400">
              No hay mapa disponible para este proyecto.
            </div>
          )}
        </div>

        <div className="w-72 flex-shrink-0">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4 sticky top-6">
            <h3 className="font-semibold text-gray-800 mb-4">Detalle del Lote</h3>
            {activeLote ? (
              <div className="space-y-3">
                <div>
                  <p className="text-xs text-gray-400">Lote</p>
                  <p className="font-medium text-gray-800">{activeLote.lote_numero}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-400">Estado</p>
                  <div className="mt-1">
                    <span
                      className="px-2.5 py-0.5 rounded-full text-xs font-medium text-white"
                      style={{ backgroundColor: colors[activeLote.lote_estado] || "#9ca3af" }}
                    >
                      {ESTADO_LOTE_LABELS[activeLote.lote_estado as keyof typeof ESTADO_LOTE_LABELS]}
                    </span>
                  </div>
                </div>
                <div>
                  <p className="text-xs text-gray-400">Precio</p>
                  <p className="font-medium text-emerald-700">{formatQ(activeLote.lote_precio)}</p>
                </div>
              </div>
            ) : (
              <p className="text-sm text-gray-400">
                Pase el mouse sobre un lote o haga clic para ver sus detalles.
              </p>
            )}

            {mapa && (
              <div className="mt-6 pt-4 border-t">
                <h4 className="text-sm font-semibold text-gray-700 mb-2">Resumen</h4>
                <div className="space-y-2 text-sm">
                  {(["disponible", "reservado", "vendido"] as const).map((estado) => {
                    const count = mapa.coordenadas.filter((c) => c.lote_estado === estado).length;
                    return (
                      <div key={estado} className="flex justify-between">
                        <span className="text-gray-500">{ESTADO_LOTE_LABELS[estado]}</span>
                        <span className="font-medium text-gray-800">{count}</span>
                      </div>
                    );
                  })}
                  <div className="flex justify-between pt-1 border-t">
                    <span className="text-gray-500 font-medium">Total</span>
                    <span className="font-bold text-gray-800">{mapa.coordenadas.length}</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
