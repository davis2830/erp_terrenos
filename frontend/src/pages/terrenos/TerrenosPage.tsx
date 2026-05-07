import MainLayout from "../../components/layout/MainLayout";

export default function TerrenosPage() {
  return (
    <MainLayout title="Inventario de Terrenos">
      <div className="bg-white rounded-xl shadow p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold">Listado de Lotes</h2>
          <button className="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700 transition-colors">
            + Nuevo Lote
          </button>
        </div>
        <p className="text-gray-500">
          Tabla de inventario de terrenos. Se implementará en la fase de codificación.
        </p>
      </div>
    </MainLayout>
  );
}
