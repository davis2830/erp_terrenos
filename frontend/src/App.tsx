import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/auth/LoginPage";
import DashboardPage from "./pages/dashboard/DashboardPage";
import TerrenosPage from "./pages/terrenos/TerrenosPage";
import MapaPage from "./pages/mapa/MapaPage";
import ClientesPage from "./pages/clientes/ClientesPage";
import FinanzasPage from "./pages/finanzas/FinanzasPage";
import FacturacionPage from "./pages/facturacion/FacturacionPage";
import ReportesPage from "./pages/reportes/ReportesPage";
import ProtectedRoute from "./components/auth/ProtectedRoute";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
        <Route path="/terrenos" element={<ProtectedRoute><TerrenosPage /></ProtectedRoute>} />
        <Route path="/mapa" element={<ProtectedRoute><MapaPage /></ProtectedRoute>} />
        <Route path="/clientes" element={<ProtectedRoute><ClientesPage /></ProtectedRoute>} />
        <Route path="/finanzas" element={<ProtectedRoute><FinanzasPage /></ProtectedRoute>} />
        <Route path="/facturacion" element={<ProtectedRoute><FacturacionPage /></ProtectedRoute>} />
        <Route path="/reportes" element={<ProtectedRoute><ReportesPage /></ProtectedRoute>} />
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
