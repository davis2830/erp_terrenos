import { useLocation, useNavigate, Link } from "react-router-dom";
import {
  LayoutDashboard,
  MapPin,
  Map,
  Users,
  DollarSign,
  FileText,
  BarChart3,
  Bell,
  LogOut,
  Menu,
} from "lucide-react";
import { useAuthStore } from "../../store/authStore";

interface SidebarProps {
  isOpen: boolean;
  onToggle: () => void;
}

const menuItems = [
  { icon: LayoutDashboard, label: "Dashboard", path: "/dashboard" },
  { icon: MapPin, label: "Terrenos", path: "/terrenos" },
  { icon: Map, label: "Mapa", path: "/mapa" },
  { icon: Users, label: "Clientes", path: "/clientes" },
  { icon: DollarSign, label: "Finanzas", path: "/finanzas" },
  { icon: FileText, label: "Facturación", path: "/facturacion" },
  { icon: BarChart3, label: "Reportes", path: "/reportes" },
  { icon: Bell, label: "Notificaciones", path: "/notificaciones" },
];

export default function Sidebar({ isOpen, onToggle }: SidebarProps) {
  const location = useLocation();
  const navigate = useNavigate();
  const logout = useAuthStore((s) => s.logout);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <aside
      className={`bg-slate-900 text-white transition-all duration-300 ${
        isOpen ? "w-64" : "w-16"
      } min-h-screen flex flex-col`}
    >
      <div className="flex items-center justify-between p-4 border-b border-slate-700">
        {isOpen && (
          <span className="text-lg font-bold text-emerald-400">GCtorque</span>
        )}
        <button onClick={onToggle} className="p-1 hover:bg-slate-700 rounded">
          <Menu size={20} />
        </button>
      </div>

      <nav className="flex-1 py-4">
        {menuItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center gap-3 px-4 py-3 transition-colors ${
                isActive
                  ? "bg-emerald-600 text-white"
                  : "hover:bg-slate-800 text-slate-300"
              }`}
            >
              <item.icon size={20} />
              {isOpen && <span>{item.label}</span>}
            </Link>
          );
        })}
      </nav>

      <div className="border-t border-slate-700 p-4">
        <button
          onClick={handleLogout}
          className="flex items-center gap-3 w-full hover:bg-slate-800 p-2 rounded transition-colors text-slate-300"
        >
          <LogOut size={20} />
          {isOpen && <span>Cerrar sesión</span>}
        </button>
      </div>
    </aside>
  );
}
