import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import authApi from '../../api/authApi';

const initialState = {
    access_token: localStorage.getItem('access_token') || null,
    refresh_token: localStorage.getItem('refresh_token') || null,
    status: 'idle',
    error: null
};

export const registerAsync = createAsyncThunk(
    'auth/register',
    async (data) => {
        const response = await authApi.register(data);
        return response.data;
    }
);

export const loginAsync = createAsyncThunk(
    'auth/login',
    async ({ username, password }) => {
        const response = await authApi.login({ username, password });
        return response.data;
    }
);

export const refreshTokenAsync = createAsyncThunk(
    'auth/refreshToken',
    async (refresh_token) => {
        const response = await authApi.refresh(refresh_token);
        return response.data;
    }
);

export const revokeAsync = createAsyncThunk(
    'auth/revoke',
    async () => {
        const response = await authApi.revoke();
        return response.data;
    }
);

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        logout(state) {
            state.access_token = null;
            state.refresh_token = null;
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
        }
    },
    extraReducers: (builder) => {
        builder
            .addCase(registerAsync.fulfilled, (state, action) => {
                // Sau khi đăng ký có thể tự động đăng nhập hoặc yêu cầu user đăng nhập lại
            })
            .addCase(loginAsync.fulfilled, (state, action) => {
                const { access_token, refresh_token } = action.payload;
                state.access_token = access_token;
                state.refresh_token = refresh_token;
                localStorage.setItem('access_token', access_token);
                localStorage.setItem('refresh_token', refresh_token);
            })
            .addCase(refreshTokenAsync.fulfilled, (state, action) => {
                const { access_token, refresh_token } = action.payload;
                state.access_token = access_token;
                state.refresh_token = refresh_token;
                localStorage.setItem('access_token', access_token);
                localStorage.setItem('refresh_token', refresh_token);
            })
            .addCase(revokeAsync.fulfilled, (state, action) => {
                state.access_token = null;
                state.refresh_token = null;
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
            });
    }
});

export const { logout } = authSlice.actions;

export default authSlice.reducer;
