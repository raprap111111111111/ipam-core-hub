import axios from "axios";
import router from "../router";

// Log this to your browser console so you can SEE the fix working
console.log("Environment API URL:", import.meta.env.VITE_API_BASE_URL);

const api = axios.create({
  // Use the variable, but we'll ensure it's exactly what we expect
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// 2. SECOND: Add the interceptors (using the variable 'api' created above)
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.clear();
      router.push("/");
    }
    return Promise.reject(error);
  }
);

// 3. THIRD: Export it
export default api;