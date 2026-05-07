import { useEffect, useState } from "react";
import { Search, Filter, Eye, X } from "lucide-react";
import MainLayout from "../../components/layout/MainLayout";
import { terrenosApi, type Lote, type Proyecto } from "../../api/endpoints/terrenos";
import { ESTADO_LOTE_COLORS, ESTADO_LOTE_LABELS } from "../../types";

function formatQ(value: number | string): string {
  const n = typeof value === "string" ? parseFloat(value) : value;
  return `Q ${n.toLocaleString("es-GT", { minimumFractionDigits: 2 })}`;
}

function EstadoBadge({ estado }: { estado: Lote["estado"] }) {
  const colors: Record<string, string> = {
    disponible: "bg-emerald-100 text-emerald-800",
    reservado: "bg-amber-100 text-amber-800",
    vendido: "bg-red-100 text-red-800",
  };
  return (
    <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${colors[estado]}`}>
      {ESTADO_LOTE_LABELS[estado]}
    </span>
  );
}

interface LoteDetailModalProps {
  lote: Lote;
  onClose: () => void;
}

function LoteDetailModal({ lote, onClose }: LoteDetailModalProps) {
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl w-full max-w-lg max-h-screen overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b">
          <h3 className="text-lg font-semibold text-gray-800">
            {lote.proyecto_nombre} - Mz.{lote.manzana} Lote {lote.numero}
          </h3>
          <button onClick={onClose} className="p-1 hover:bg-gray-100 rounded">
            <X size={20} />
          </button>
        </div>
        <div className="p-6 space-y-4">
          <div className="flex justify-between">
            <span className="text-gray-500">Estado</span>
            <EstadoBadge estado={lote.estado} />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-xs text-gray-400">Medida Frente</p>
              <p className="font-medium">{lote.medida_frente} m</p>
            </div>
            <div>
              <p className="text-xs text-gray-400">Medida Fondo</p>
              <p className="font-medium">{lote.medida_fondo} m</p>
            </div>
            <div>
              <p className="text-xs text-gray-400">Área Total</p>
              <p className="font-medium">{lote.area_total} m²</p>
            </div>
            <div>
              <p className="text-xs text-gray-400">Precio Base</p>
              <p className="font-medium text-emerald-700">{formatQ(lote.precio_base)}</p>
            </div>
          </div>
          {(lote.num_finca || lote.folio || lote.libro) && (
            <div className="border-t pt-4">
              <h4 className="text-sm font-semibold text-gray-700 mb-2">Datos Registrales</h4>
              <div className="grid grid-cols-3 gap-3">
                <div>
                  <p className="text-xs text-gray-400">No. Finca</p>
                  <p className="text-sm">{lote.num_finca || "-"}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-400">Folio</p>
                  <p className="text-sm">{lote.folio || "-"}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-400">Libro</p>
                  <p className="text-sm">{lote.libro || "-"}</p>
                </div>
              </div>
            </div>
          )}
          {lote.notas && (
            <div className="border-t pt-4">
              <h4 className="text-sm font-semibold text-gray-700 mb-1">Notas</h4>
              <p className="text-sm text-gray-600">{lote.notas}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function TerrenosPage() {
  const [lotes, setLotes] = useState<Lote[]>([]);
  const [proyectos, setProyectos] = useState<Proyecto[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedLote, setSelectedLote] = useState<Lote | null>(null);
  const [search, setSearch] = useState("");
  const [estadoFilter, setEstadoFilter] = useState("");
  const [proyectoFilter, setProyectoFilter] = useState("");
  const [page, setPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const pageSize = 10;

  useEffect(() => {
    terrenosApi.listProyectos().then((res) => setProyectos(res.data.results)).catch(() => {});
  }, []);

  useEffect(() => {
    setLoading(true);
    const params: Record<string, string> = { page: String(page), page_size: String(pageSize) };
    if (search) params.search = search;
    if (estadoFilter) params.estado = estadoFilter;
    if (proyectoFilter) params.proyecto = proyectoFilter;

    terrenosApi.listLotes(params)
      .then((res) => {
        setLotes(res.data.results);
        setTotalCount(res.data.count);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [page, search, estadoFilter, proyectoFilter]);

  const handleViewDetail = (lote: Lote) => {
    if (lote.fotografias !== undefined) {
      setSelectedLote(lote);
      return;
    }
    terrenosApi.getLote(lote.id).then((res) => setSelectedLote(res.data)).catch(() => {});
  };

  const totalPages = Math.ceil(totalCount / pageSize);

  const stats = {
    disponibles: lotes.filter((l) => l.estado === "disponible").length,
    reservados: lotes.filter((l) => l.estado === "reservado").length,
    vendidos: lotes.filter((l) => l.estado === "vendido").length,
  };

  return (
    <MainLayout title="Inventario de Terrenos">
      <div className="grid grid-cols-3 gap-4 mb-6">
        {[
          { label: "Disponibles", count: stats.disponibles, color: ESTADO_LOTE_COLORS.disponible },
          { label: "Reservados", count: stats.reservados, color: ESTADO_LOTE_COLORS.reservado },
          { label: "Vendidos", count: stats.vendidos, color: ESTADO_LOTE_COLORS.vendido },
        ].map((s) => (
          <div key={s.label} className="bg-white rounded-lg shadow-sm p-4 border border-gray-100 flex items-center gap-3">
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: s.color }} />
            <div>
              <p className="text-2xl font-bold text-gray-800">{s.count}</p>
              <p className="text-xs text-gray-500">{s.label}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100">
        <div className="p-4 border-b border-gray-100 flex flex-wrap gap-3 items-center">
          <div className="relative flex-1 min-w-48">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="Buscar por número, manzana, finca..."
              value={search}
              onChange={(e) => { setSearch(e.target.value); setPage(1); }}
              className="w-full pl-9 pr-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none"
            />
          </div>
          <div className="flex items-center gap-2">
            <Filter size={16} className="text-gray-400" />
            <select
              value={estadoFilter}
              onChange={(e) => { setEstadoFilter(e.target.value); setPage(1); }}
              className="border border-gray-300 rounded-lg px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-emerald-500"
            >
              <option value="">Todos los estados</option>
              <option value="disponible">Disponible</option>
              <option value="reservado">Reservado</option>
              <option value="vendido">Vendido</option>
            </select>
            <select
              value={proyectoFilter}
              onChange={(e) => { setProyectoFilter(e.target.value); setPage(1); }}
              className="border border-gray-300 rounded-lg px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-emerald-500"
            >
              <option value="">Todos los proyectos</option>
              {proyectos.map((p) => (
                <option key={p.id} value={String(p.id)}>{p.nombre}</option>
              ))}
            </select>
          </div>
        </div>

        {loading ? (
          <div className="flex items-center justify-center h-48">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-600" />
          </div>
        ) : (
          <>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="text-left px-4 py-3 text-xs font-medium text-gray-500 uppercase">Lote</th>
                    <th className="text-left px-4 py-3 text-xs font-medium text-gray-500 uppercase">Manzana</th>
                    <th className="text-left px-4 py-3 text-xs font-medium text-gray-500 uppercase">Proyecto</th>
                    <th className="text-left px-4 py-3 text-xs font-medium text-gray-500 uppercase">Área (m²)</th>
                    <th className="text-left px-4 py-3 text-xs font-medium text-gray-500 uppercase">Precio</th>
                    <th className="text-left px-4 py-3 text-xs font-medium text-gray-500 uppercase">Estado</th>
                    <th className="text-center px-4 py-3 text-xs font-medium text-gray-500 uppercase">Acciones</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {lotes.map((lote) => (
                    <tr key={lote.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-4 py-3 text-sm font-medium text-gray-900">{lote.numero}</td>
                      <td className="px-4 py-3 text-sm text-gray-600">{lote.manzana}</td>
                      <td className="px-4 py-3 text-sm text-gray-600">{lote.proyecto_nombre}</td>
                      <td className="px-4 py-3 text-sm text-gray-600">{lote.area_total}</td>
                      <td className="px-4 py-3 text-sm font-medium text-gray-900">{formatQ(lote.precio_base)}</td>
                      <td className="px-4 py-3"><EstadoBadge estado={lote.estado} /></td>
                      <td className="px-4 py-3 text-center">
                        <button
                          onClick={() => handleViewDetail(lote)}
                          className="p-1.5 hover:bg-emerald-50 rounded-lg text-emerald-600 transition-colors"
                          title="Ver detalle"
                        >
                          <Eye size={16} />
                        </button>
                      </td>
                    </tr>
                  ))}
                  {lotes.length === 0 && (
                    <tr>
                      <td colSpan={7} className="text-center py-8 text-gray-400">
                        No se encontraron lotes con los filtros aplicados.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            {totalPages > 1 && (
              <div className="flex items-center justify-between px-4 py-3 border-t border-gray-100">
                <p className="text-sm text-gray-500">
                  Mostrando {(page - 1) * pageSize + 1}-{Math.min(page * pageSize, totalCount)} de {totalCount}
                </p>
                <div className="flex gap-1">
                  <button
                    onClick={() => setPage(Math.max(1, page - 1))}
                    disabled={page === 1}
                    className="px-3 py-1 text-sm border rounded-lg disabled:opacity-50 hover:bg-gray-50"
                  >
                    Anterior
                  </button>
                  {Array.from({ length: Math.min(totalPages, 5) }, (_, i) => i + 1).map((p) => (
                    <button
                      key={p}
                      onClick={() => setPage(p)}
                      className={`px-3 py-1 text-sm border rounded-lg ${
                        p === page ? "bg-emerald-600 text-white border-emerald-600" : "hover:bg-gray-50"
                      }`}
                    >
                      {p}
                    </button>
                  ))}
                  <button
                    onClick={() => setPage(Math.min(totalPages, page + 1))}
                    disabled={page === totalPages}
                    className="px-3 py-1 text-sm border rounded-lg disabled:opacity-50 hover:bg-gray-50"
                  >
                    Siguiente
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {selectedLote && (
        <LoteDetailModal lote={selectedLote} onClose={() => setSelectedLote(null)} />
      )}
    </MainLayout>
  );
}
