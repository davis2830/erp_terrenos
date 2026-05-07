import { useEffect, useState } from "react";
import { MapPin, DollarSign, ShoppingCart, TrendingUp } from "lucide-react";
import MainLayout from "../../components/layout/MainLayout";
import { dashboardApi, type DashboardStats } from "../../api/endpoints/mapa";

function formatQ(value: number): string {
  return `Q ${value.toLocaleString("es-GT", { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
}

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    dashboardApi.getStats()
      .then((res) => setStats(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <MainLayout title="Dashboard">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-600" />
        </div>
      </MainLayout>
    );
  }

  const kpis = stats
    ? [
        { label: "Lotes Disponibles", value: String(stats.lotes.disponibles), icon: MapPin, color: "bg-emerald-500", sub: `de ${stats.lotes.total} totales` },
        { label: "Lotes Reservados", value: String(stats.lotes.reservados), icon: ShoppingCart, color: "bg-amber-500", sub: `${stats.lotes.total ? Math.round((stats.lotes.reservados / stats.lotes.total) * 100) : 0}% del inventario` },
        { label: "Lotes Vendidos", value: String(stats.lotes.vendidos), icon: ShoppingCart, color: "bg-red-500", sub: `${stats.lotes.total ? Math.round((stats.lotes.vendidos / stats.lotes.total) * 100) : 0}% del inventario` },
        { label: "Valor Vendido", value: formatQ(stats.valores.vendido), icon: DollarSign, color: "bg-blue-500", sub: "ventas acumuladas" },
      ]
    : [];

  return (
    <MainLayout title="Dashboard">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {kpis.map((kpi) => (
          <div key={kpi.label} className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-medium text-gray-500">{kpi.label}</h3>
              <div className={`${kpi.color} p-2 rounded-lg`}>
                <kpi.icon size={20} className="text-white" />
              </div>
            </div>
            <p className="text-2xl font-bold text-gray-800">{kpi.value}</p>
            <p className="text-xs text-gray-400 mt-1">{kpi.sub}</p>
          </div>
        ))}
      </div>

      {stats && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Distribución de Inventario</h3>
            <div className="space-y-4">
              {[
                { label: "Disponibles", count: stats.lotes.disponibles, color: "bg-emerald-500" },
                { label: "Reservados", count: stats.lotes.reservados, color: "bg-amber-500" },
                { label: "Vendidos", count: stats.lotes.vendidos, color: "bg-red-500" },
              ].map((item) => (
                <div key={item.label}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-600">{item.label}</span>
                    <span className="font-medium text-gray-800">
                      {item.count} ({stats.lotes.total ? Math.round((item.count / stats.lotes.total) * 100) : 0}%)
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div
                      className={`${item.color} h-2.5 rounded-full transition-all`}
                      style={{ width: `${stats.lotes.total ? (item.count / stats.lotes.total) * 100 : 0}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Resumen Financiero</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <span className="text-gray-600 text-sm">Valor Total Inventario</span>
                <span className="font-bold text-gray-800">{formatQ(stats.valores.total)}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-emerald-50 rounded-lg">
                <span className="text-gray-600 text-sm">Total Vendido</span>
                <span className="font-bold text-emerald-700">{formatQ(stats.valores.vendido)}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-amber-50 rounded-lg">
                <span className="text-gray-600 text-sm">Disponible por Vender</span>
                <span className="font-bold text-amber-700">{formatQ(stats.valores.disponible)}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                <span className="text-gray-600 text-sm">Proyectos Activos</span>
                <span className="font-bold text-blue-700">{stats.proyectos_activos}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp size={18} className="text-emerald-600" />
            <h3 className="text-lg font-semibold text-gray-800">Ventas Recientes</h3>
          </div>
          <p className="text-gray-400 text-sm">Se habilitará con el módulo de CRM y Ventas.</p>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
          <div className="flex items-center gap-2 mb-2">
            <DollarSign size={18} className="text-blue-600" />
            <h3 className="text-lg font-semibold text-gray-800">Pagos Próximos</h3>
          </div>
          <p className="text-gray-400 text-sm">Se habilitará con el módulo de Finanzas.</p>
        </div>
      </div>
    </MainLayout>
  );
}
