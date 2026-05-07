import MainLayout from "../../components/layout/MainLayout";

export default function FacturacionPage() {
  return (
    <MainLayout title="Facturación y Documentos">
      <div className="bg-white rounded-xl shadow p-6">
        <h2 className="text-lg font-semibold mb-4">Facturación Electrónica</h2>
        <p className="text-gray-500">
          Integración FEL/SAT y gestor documental. Se implementará en la fase de codificación.
        </p>
      </div>
    </MainLayout>
  );
}
