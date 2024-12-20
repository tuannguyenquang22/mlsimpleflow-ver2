import axiosClient from './axiosClient';

const authApi = {
    register(data) {
        // data = {display_name, email, password}
        return axiosClient.post('/users', data);
    },
    login(data) {
        // data = {username, password}, content-type: application/x-www-form-urlencoded
        const form = new URLSearchParams(data);
        return axiosClient.post('/login/oauth', form, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });
    },
    refresh(refresh_token) {
        const form = new URLSearchParams({ refresh_token });
        return axiosClient.post('/login/refresh', form, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });
    },
    revoke() {
        return axiosClient.post('/revoke');
    }
};

export default authApi;
