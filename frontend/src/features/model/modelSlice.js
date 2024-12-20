import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import modelApi from '../../api/modelApi';

export const fetchMetadataAsync = createAsyncThunk(
    'model/fetchMetadata',
    async () => {
        const response = await modelApi.getMetadata();
        return response.data;
    }
);


export const fetchAllTasksAsync = createAsyncThunk(
    'model/fetchAllTasks',
    async () => {
        const response = await modelApi.getAllTasks();
        return response.data;
    }
);


export const createModelTaskAsync = createAsyncThunk(
    'model/createTask',
    async (taskData) => {
        const response = await modelApi.createTask(taskData);
        return response.data;
    }
);


export const fetchAllResultsAsync = createAsyncThunk(
    'model/fetchAllResults',
    async () => {
        const response = await modelApi.getAllResults();
        return response.data;
    }
);


export const runTaskAsync = createAsyncThunk(
    'model/runTask',
    async (taskId) => {
        const response = await modelApi.runTask(taskId);
        return response.data;
    }
);


const modelSlice = createSlice({
    name: 'model',
    initialState: {
        metadata: null,
        status: 'idle',
        taskListStatus: 'idle',
        taskList: [],
        resultListStatus: 'idle',
        resultList: [],
        runTaskStatus: 'idle',
        runTaskError: null,
        error: null,
        createTaskStatus: 'idle',
        createTaskError: null
    },
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(fetchMetadataAsync.pending, (state) => {
                state.status = 'loading';
            })
            .addCase(fetchMetadataAsync.fulfilled, (state, action) => {
                state.status = 'succeeded';
                state.metadata = action.payload;
            })
            .addCase(fetchMetadataAsync.rejected, (state, action) => {
                state.status = 'failed';
                state.error = action.error.message;
            })

            .addCase(createModelTaskAsync.pending, (state) => {
                state.createTaskStatus = 'loading';
            })
            .addCase(createModelTaskAsync.fulfilled, (state, action) => {
                state.createTaskStatus = 'succeeded';
            })
            .addCase(createModelTaskAsync.rejected, (state, action) => {
                state.createTaskStatus = 'failed';
                state.createTaskError = action.error.message;
            })

            .addCase(fetchAllTasksAsync.pending, (state) => {
                state.taskListStatus = 'loading';
            })
            .addCase(fetchAllTasksAsync.fulfilled, (state, action) => {
                state.taskListStatus = 'succeeded';
                state.taskList = action.payload;
            })
            .addCase(fetchAllTasksAsync.rejected, (state, action) => {
                state.taskListStatus = 'failed';
                state.error = action.error.message;
            })

            .addCase(fetchAllResultsAsync.pending, (state) => {
                state.resultListStatus = 'loading';
            })
            .addCase(fetchAllResultsAsync.fulfilled, (state, action) => {
                state.resultListStatus = 'succeeded';
                state.resultList = action.payload;
            })
            .addCase(fetchAllResultsAsync.rejected, (state, action) => {
                state.resultListStatus = 'failed';
                state.error = action.error.message;
            })

            .addCase(runTaskAsync.pending, (state) => {
                state.runTaskStatus = 'loading';
            })
            .addCase(runTaskAsync.fulfilled, (state) => {
                state.runTaskStatus = 'succeeded';
            })
            .addCase(runTaskAsync.rejected, (state, action) => {
                state.runTaskStatus = 'failed';
                state.runTaskError = action.error.message;
            })

    }
});

export default modelSlice.reducer;