import MainLayout from "../../components/layout/MainLayout";

export default function ClientesPage() {
  return (
    <MainLayout title="Gestión de Clientes">
      <div className="bg-white rounded-xl shadow p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold">Directorio de Clientes</h2>
          <button className="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700 transition-colors">
            + Nuevo Cliente
          </button>
        </div>
        <p className="text-gray-500">
          CRM y directorio de clientes. Se implementará en la fase de codificación.
        </p>
      </div>
    </MainLayout>
  );
}
