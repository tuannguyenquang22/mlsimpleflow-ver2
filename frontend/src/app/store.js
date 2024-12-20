import { configureStore } from '@reduxjs/toolkit';
import authReducer from '../features/auth/authSlice';
import datasetReducer from '../features/dataset/datasetSlice';
import modelReducer from '../features/model/modelSlice';

export const store = configureStore({
    reducer: {
        auth: authReducer,
        dataset: datasetReducer,
        model: modelReducer,
    },
});
