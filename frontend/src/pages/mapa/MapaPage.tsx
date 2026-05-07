import MainLayout from "../../components/layout/MainLayout";

export default function MapaPage() {
  return (
    <MainLayout title="Mapa Interactivo">
      <div className="bg-white rounded-xl shadow p-6">
        <h2 className="text-lg font-semibold mb-4">Mapa de Lotificación</h2>
        <div className="border-2 border-dashed border-gray-300 rounded-lg h-96 flex items-center justify-center">
          <p className="text-gray-400">
            Visualizador SVG interactivo. Se implementará en la fase de codificación.
          </p>
        </div>
      </div>
    </MainLayout>
  );
}
