import MainLayout from "../../components/layout/MainLayout";

export default function FinanzasPage() {
  return (
    <MainLayout title="Cartera y Financiamiento">
      <div className="bg-white rounded-xl shadow p-6">
        <h2 className="text-lg font-semibold mb-4">Control de Pagos</h2>
        <p className="text-gray-500">
          Planes de pago, cuotas y cobranza. Se implementará en la fase de codificación.
        </p>
      </div>
    </MainLayout>
  );
}
