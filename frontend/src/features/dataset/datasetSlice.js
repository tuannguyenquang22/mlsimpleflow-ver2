import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import datasetApi from '../../api/datasetApi';

const initialState = {
    uploadStatus: 'idle',
    preprocessStatus: 'idle',
    listStatus: 'idle',
    error: null,
    uploadedDataset: null,
    datasetList: []
};

export const uploadDatasetAsync = createAsyncThunk(
    'dataset/upload',
    async ({ dataset_type, file }) => {
        const response = await datasetApi.upload(dataset_type, file);
        return response.data; // giả sử trả về dataset_id,...
    }
);

export const preprocessDatasetAsync = createAsyncThunk(
    'dataset/preprocess',
    async ({ dataset_id, target_column }) => {
        const response = await datasetApi.preprocess(dataset_id, target_column);
        return response.data;
    }
);

export const fetchDatasetsAsync = createAsyncThunk(
    'dataset/fetchList',
    async (dataset_type) => {
        const response = await datasetApi.getDatasets(dataset_type);
        return response.data
    }
)

const datasetSlice = createSlice({
    name: 'dataset',
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(uploadDatasetAsync.pending, (state) => {
                state.uploadStatus = 'loading';
            })
            .addCase(uploadDatasetAsync.fulfilled, (state, action) => {
                state.uploadStatus = 'succeeded';
                state.uploadedDataset = action.payload; // { dataset_id: ... }
            })
            .addCase(uploadDatasetAsync.rejected, (state, action) => {
                state.uploadStatus = 'failed';
                state.error = action.error.message;
            })
            .addCase(preprocessDatasetAsync.pending, (state) => {
                state.preprocessStatus = 'loading';
            })
            .addCase(preprocessDatasetAsync.fulfilled, (state, action) => {
                state.preprocessStatus = 'succeeded';
                // trả về kết quả preprocess
            })
            .addCase(preprocessDatasetAsync.rejected, (state, action) => {
                state.preprocessStatus = 'failed';
                state.error = action.error.message;
            })
            .addCase(fetchDatasetsAsync.pending, (state) => {
                state.listStatus = 'loading';
            })
            .addCase(fetchDatasetsAsync.fulfilled, (state, action) => {
                state.listStatus = 'succeeded';
                state.datasetList = action.payload;
            })
            .addCase(fetchDatasetsAsync.rejected, (state, action) => {
                state.listStatus = 'failed';
                state.error = action.error.message;
            })
    }
});

export default datasetSlice.reducer;
