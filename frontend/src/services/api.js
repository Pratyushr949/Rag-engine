import axios from "axios";

// Default API URL fallback for development
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-type": "application/json",
  },
});

export const uploadDocument = async (file, onUploadProgress) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await apiClient.post("/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
    onUploadProgress,
  });
  return response.data;
};

export const chatWithBot = async (message, history) => {
  const response = await apiClient.post("/chat", {
    message,
    history,
  });
  return response.data;
};

export const resetSystem = async () => {
  const response = await apiClient.delete("/reset");
  return response.data;
};
