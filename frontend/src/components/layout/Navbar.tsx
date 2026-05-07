import { Bell, User } from "lucide-react";
import { useAuthStore } from "../../store/authStore";

interface NavbarProps {
  title: string;
}

const ROLE_LABELS: Record<string, string> = {
  admin: "Administrador",
  gerente: "Gerente",
  vendedor: "Vendedor",
};

export default function Navbar({ title }: NavbarProps) {
  const user = useAuthStore((s) => s.user);

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
      <h1 className="text-xl font-semibold text-gray-800">{title}</h1>

      <div className="flex items-center gap-4">
        <button className="relative p-2 hover:bg-gray-100 rounded-full">
          <Bell size={20} className="text-gray-600" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
        </button>

        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-emerald-500 rounded-full flex items-center justify-center">
            <User size={16} className="text-white" />
          </div>
          <div className="text-sm">
            <p className="text-gray-700 font-medium">
              {user?.full_name || "Usuario"}
            </p>
            <p className="text-gray-400 text-xs">
              {user?.role ? ROLE_LABELS[user.role] || user.role : ""}
            </p>
          </div>
        </div>
      </div>
    </header>
  );
}
