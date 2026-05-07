import { useCallback, useEffect } from "react";
import { authApi } from "../api/endpoints/auth";
import { useAuthStore } from "../store/authStore";

export function useAuth() {
  const { user, isAuthenticated, isLoading, login, logout, setUser, setLoading } =
    useAuthStore();

  const loadUser = useCallback(async () => {
    if (!isAuthenticated) {
      setLoading(false);
      return;
    }
    try {
      const response = await authApi.getProfile();
      setUser(response.data);
    } catch {
      logout();
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated, setUser, logout, setLoading]);

  useEffect(() => {
    loadUser();
  }, [loadUser]);

  const handleLogin = async (email: string, password: string) => {
    const response = await authApi.login({ email, password });
    const { access, refresh } = response.data;
    const profileResponse = await authApi.getProfile();
    login(access, refresh, profileResponse.data);
  };

  const handleLogout = async () => {
    try {
      await authApi.logout();
    } finally {
      logout();
    }
  };

  return {
    user,
    isAuthenticated,
    isLoading,
    login: handleLogin,
    logout: handleLogout,
  };
}
