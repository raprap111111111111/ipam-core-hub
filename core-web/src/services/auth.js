import api from "./api";

// No need for "me/" or "login/" headers here, api.js handles it!
export const loginUser = async (payload) => {
  const response = await api.post("/accounts/login/", payload);
  return response.data;
};

export const getMe = async () => {
  const response = await api.get("/accounts/me/");
  return response.data;
};

export const logoutUser = async () => {
  const refresh = localStorage.getItem("refresh_token");
  return api.post("/accounts/logout/", { refresh });
};

export const changeUserPassword = async (payload) => {
  const response = await api.post("/accounts/change-password/", payload);
  return response.data;
};

// Optional: Refresh user data (useful after profile update)
export const refreshUser = async () => {
  const response = await api.get("/accounts/me/");
  return response.data;
};