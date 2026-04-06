import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8001/api/accounts/",
  headers: {
    "Content-Type": "application/json",
  },
});

export const loginUser = async (payload) => {
  const response = await API.post("login/", payload);
  return response.data;
};

export const getMe = async () => {
  const token = localStorage.getItem("access_token");
  const response = await API.get("me/", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};

export const logoutUser = async () => {
  const access = localStorage.getItem("access_token");
  const refresh = localStorage.getItem("refresh_token");

  return API.post(
    "logout/",
    { refresh },
    {
      headers: {
        Authorization: `Bearer ${access}`,
      },
    }
  );
};

export default API;