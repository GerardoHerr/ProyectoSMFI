import axios from "axios";

const api = axios.create({
    baseURL: 'http://localhost:8000/api',
});

export const crearAlerta = (data) => {
    return api.post("/alertas/", data);
}

export const listarAlertas = (params = {}) => {
    return api.get("/alertas/", { params });
}

export const modificarAlerta = (id, data) => {
    return api.patch(`/alertas/${id}/`, data);
}

