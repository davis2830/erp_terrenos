import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/auth/LoginPage";
import DashboardPage from "./pages/dashboard/DashboardPage";
import TerrenosPage from "./pages/terrenos/TerrenosPage";
import MapaPage from "./pages/mapa/MapaPage";
import ClientesPage from "./pages/clientes/ClientesPage";
import FinanzasPage from "./pages/finanzas/FinanzasPage";
import FacturacionPage from "./pages/facturacion/FacturacionPage";
import ReportesPage from "./pages/reportes/ReportesPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/terrenos" element={<TerrenosPage />} />
        <Route path="/mapa" element={<MapaPage />} />
        <Route path="/clientes" element={<ClientesPage />} />
        <Route path="/finanzas" element={<FinanzasPage />} />
        <Route path="/facturacion" element={<FacturacionPage />} />
        <Route path="/reportes" element={<ReportesPage />} />
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
