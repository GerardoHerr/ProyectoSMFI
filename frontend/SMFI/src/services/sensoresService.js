import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api',
});

export const getSensores = () => {
    return api.get('/sensores/');
}

