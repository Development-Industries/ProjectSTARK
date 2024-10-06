import axios from 'axios';

const API = axios.create({ baseURL: 'http://localhost:5000/api' });

API.interceptors.request.use((req) => {
    const token = localStorage.getItem('token');
    if (token) {
        req.headers.Authorization = `Bearer ${token}`;
    }
    return req;
});

export const login = (credentials) => API.post('/users/login', credentials);
export const register = (data) => API.post('/users/register', data);
export const getHealthData = () => API.get('/users/health-data');
// Add other API calls as needed
