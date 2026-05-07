import apiClient from "../client";

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
}

export interface UserProfile {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  full_name: string;
  phone: string;
  role: "admin" | "gerente" | "vendedor";
  avatar: string | null;
}

export const authApi = {
  login: (data: LoginRequest) =>
    apiClient.post<LoginResponse>("/auth/login/", data),

  refresh: (refreshToken: string) =>
    apiClient.post<{ access: string }>("/auth/refresh/", {
      refresh: refreshToken,
    }),

  getProfile: () => apiClient.get<UserProfile>("/auth/me/"),

  updateProfile: (data: Partial<UserProfile>) =>
    apiClient.patch<UserProfile>("/auth/me/", data),

  logout: () => apiClient.post("/auth/logout/"),
};
