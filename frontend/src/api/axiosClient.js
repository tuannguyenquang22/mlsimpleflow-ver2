// Thiết lập axios client với interceptor cho việc refresh token tự động:

import axios from 'axios';
import { store } from '../app/store';
import { logout, refreshTokenAsync } from '../features/auth/authSlice';


const axiosClient = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
    headers: {
        'Content-Type': 'application/json',
    },
});

let isRefreshing = false;
let refreshSubscribers = [];

const onRrefreshed = (token) => {
    refreshSubscribers.map((callback) => callback(token));
    refreshSubscribers = [];
};

axiosClient.interceptors.request.use((config) => {
    const state = store.getState();
    const token = state.auth.access_token;
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, error => {
    return Promise.reject(error);
});

axiosClient.interceptors.response.use((response) => {
    return response;
}, async (error) => {
    const { config, response } = error;
    if (response && response.status === 401 && !config._retry) {
        if (!isRefreshing) {
            isRefreshing = true;
            const state = store.getState();
            const rToken = state.auth.refresh_token;
            try {
                const newToken = await store.dispatch(refreshTokenAsync(rToken)).unwrap();
                isRefreshing = false;
                onRrefreshed(newToken.access_token);
            } catch (err) {
                isRefreshing = false;
                store.dispatch(logout());
                return Promise.reject(err);
            }
        }

        const retryOriginalRequest = new Promise((resolve) => {
            refreshSubscribers.push((token) => {
                config.headers.Authorization = 'Bearer ' + token;
                resolve(axiosClient(config));
            });
        });
        return retryOriginalRequest;
    }
    return Promise.reject(error);
});

export default axiosClient;

