import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: { "Content-Type": "application/json" },
});

export const notesService = {
  getAll: (params = {}) => api.get("/notes/", { params }).then((r) => r.data),
  getById: (id) => api.get(`/notes/${id}`).then((r) => r.data),
  create: (data) => api.post("/notes/", data).then((r) => r.data),
  update: (id, data) => api.put(`/notes/${id}`, data).then((r) => r.data),
  delete: (id) => api.delete(`/notes/${id}`),
  getTags: () => api.get("/notes/tags/all").then((r) => r.data),
};
