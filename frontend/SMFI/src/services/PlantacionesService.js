import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api',
});

export const getPlantaciones = () => {
    return api.get('/plantaciones/');
}

export const getPlantacionById = (id) => {
    return api.get('/plantaciones/' + id + '/');
}

export const getSensoresByPlantacionId = (plantacionId, ultimoValor) => {
    return api.get('/plantaciones/' + plantacionId + '/sensores/' + ultimoValor);
}

export const createPlantacion = (data) => {
    return api.post('/plantaciones/', data);
}

export const updatePlantacion = (id, data) => {
    return api.put('/plantaciones/' + id + '/', data);
}

export const deletePlantacion = (id) => {
    return api.delete('/plantaciones/' + id + '/');
}