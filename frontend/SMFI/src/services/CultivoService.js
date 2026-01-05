import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api',
});

export const getCultivoById = (id) => {
    return api.get("/cultivos/" + id);
}

export const getCultivos = () => {
    return api.get("/cultivos/");
}