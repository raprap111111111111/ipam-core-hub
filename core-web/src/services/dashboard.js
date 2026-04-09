import axios from "axios";

// Removed the trailing slash from base URL for cleaner concatenation
const API_URL = "http://127.0.0.1:8002/api";

export async function getDashboardSummary() {
  const token = localStorage.getItem("access_token");

  try {
    const response = await axios.get(`${API_URL}/dashboard/summary/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    // Check if the backend success flag is true
    if (response.data && response.data.success) {
      return response.data.data;
    }
    
    throw new Error(response.data.message || "Failed to fetch dashboard data");
  } catch (error) {
    console.error("API Error in getDashboardSummary:", error.response?.data || error.message);
    throw error; // Re-throw so the Vue component can catch it
  }
}