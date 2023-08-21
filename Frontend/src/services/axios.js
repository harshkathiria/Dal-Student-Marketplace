import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://localhost:5000", // Replace with your API base URL
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
  withCredentials:true,

});

apiClient.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });
  

export default apiClient;

