import axiosClient from './axiosClient';

const datasetApi = {
    upload(dataset_type, file) {
        const formData = new FormData();
        formData.append('dataset_type', 'raw');
        formData.append('file', file);
        return axiosClient.post('/dataset/v1/datasets/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
    },
    preprocess(dataset_id, target_column) {
        const form = new URLSearchParams({ target_column });
        return axiosClient.post(`/dataset/v1/datasets/${dataset_id}/preprocessing`, form, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });
    },
    getDatasets(dataset_type) {
        return axiosClient.get(`/dataset/v1/datasets/${dataset_type}`);
    }
};

export default datasetApi;
