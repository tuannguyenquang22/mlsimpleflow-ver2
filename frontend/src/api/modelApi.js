import axiosClient from "./axiosClient";

const modelApi = {
    getMetadata() {
        return axiosClient.get("/model/v3.10/metadata");
    },
    createTask(taskData) {
        return axiosClient.post("/model/v1/tasks", taskData);
    },
    getAllTasks() {
        return axiosClient.get("/model/v1/tasks")
    },
    getAllResults() {
        return axiosClient.get("/model/v1/results")
    },
    runTask(taskId) {
        return axiosClient.post(`/model/v1/tasks/${taskId}/run`)
    }
};

export default modelApi;