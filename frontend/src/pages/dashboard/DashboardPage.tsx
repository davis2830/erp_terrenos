import MainLayout from "../../components/layout/MainLayout";

export default function DashboardPage() {
  return (
    <MainLayout title="Dashboard">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {/* Placeholder: Tarjetas de métricas */}
        <MetricCard title="Lotes Disponibles" value="--" color="emerald" />
        <MetricCard title="Lotes Reservados" value="--" color="amber" />
        <MetricCard title="Lotes Vendidos" value="--" color="red" />
        <MetricCard title="Ingresos del Mes" value="Q --" color="blue" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Ventas Recientes</h2>
          <p className="text-gray-500">Se implementará en la fase de codificación.</p>
        </div>
        <div className="bg-white rounded-xl shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Pagos Próximos</h2>
          <p className="text-gray-500">Se implementará en la fase de codificación.</p>
        </div>
      </div>
    </MainLayout>
  );
}

function MetricCard({
  title,
  value,
  color,
}: {
  title: string;
  value: string;
  color: string;
}) {
  const colorMap: Record<string, string> = {
    emerald: "bg-emerald-50 text-emerald-700 border-emerald-200",
    amber: "bg-amber-50 text-amber-700 border-amber-200",
    red: "bg-red-50 text-red-700 border-red-200",
    blue: "bg-blue-50 text-blue-700 border-blue-200",
  };

  return (
    <div className={`rounded-xl border p-6 ${colorMap[color]}`}>
      <p className="text-sm font-medium opacity-75">{title}</p>
      <p className="text-3xl font-bold mt-2">{value}</p>
    </div>
  );
}
