import React, { useEffect, useState } from 'react';
import { Form, Input, Select, Button, Card, message, InputNumber, Space, Switch } from 'antd';
import { useDispatch, useSelector } from 'react-redux';
import { fetchMetadataAsync, createModelTaskAsync } from '../features/model/modelSlice';
import { fetchDatasetsAsync } from '../features/dataset/datasetSlice';
import { Cron } from 'react-js-cron'
import 'react-js-cron/dist/styles.css'


function TaskCreationPage() {
    const dispatch = useDispatch();
    const { metadata, status, error, createTaskStatus, createTaskError } = useSelector(state => state.model);
    const { datasetList, listStatus, errorDataset } = useSelector(state => state.dataset)

    const [form] = Form.useForm();

    const [selectedModelName, setSelectedModelName] = useState(null);

    const [cronValue, setCronValue] = useState("30 5 * * 1,6");
    const [isUseCron, setIsUseCron] = useState(false);

    const [selectedTaskType, setSelectedTaskType] = useState(null);
    const [selectedProblemType, setSelectedProblemType] = useState(null);

    useEffect(() => {
        dispatch(fetchDatasetsAsync("preprocessed"))
        if (!metadata) {
            dispatch(fetchMetadataAsync());
        }
    }, [dispatch, metadata]);


    const handleFinish = (values) => {
        const { name, task_type, dataset_id, cron_expression } = values;

        let modelParams = {};

        if (task_type === 'train') {
            // Lấy từ training_params
            const trainingParams = values.training_params || [];
            trainingParams.forEach(item => {
                // Ví dụ { hyperparam_name: "n_estimators", value: 100 }
                modelParams[item.hyperparam_name] = item.value;
            });
        } else if (task_type === 'tune') {
            // tuning mode
            const tuningParams = values.tuning_params || [];
            // Lấy num_trials
            const { num_trials } = values;
            modelParams.num_trials = num_trials; // thêm num_trials

            tuningParams.forEach(item => {
                const { hyperparam_name, param_type } = item;
                if (param_type === 'int' || param_type === 'float') {
                    // cần lower, upper
                    modelParams[hyperparam_name] = [param_type, item.lower, item.upper];
                } else if (param_type === 'choice') {
                    // cần tách chuỗi choices
                    const choiceValues = item.choices.split(';').map(c => c.trim()).filter(c => c);
                    modelParams[hyperparam_name] = [param_type, ...choiceValues];
                }
            });
        }

        const taskData = {
            name,
            task_type,
            dataset_id,
            model_names: [selectedModelName],
            model_params: [modelParams],
            cron_expression: isUseCron ? cronValue : null
        };

        console.log(taskData)

        dispatch(createModelTaskAsync(taskData))
            .unwrap()
            .then(() => {
                message.success("Tạo task thành công!");
                form.resetFields();
                setSelectedModelName(null);
                setSelectedTaskType(null);
            })
            .catch(err => {
                message.error("Tạo task thất bại: " + err);
            });
    };

    const modelNames = metadata ? Object.keys(metadata) : [];
    const getHyperparamOptions = () => {
        if (selectedModelName && selectedProblemType && metadata) {
            const paramsObj = JSON.parse(metadata[selectedModelName][selectedProblemType]);
            return Object.keys(paramsObj).map(hp => ({ label: hp, value: hp }));
        }
        return [];
    };

    const handleDatasetChange = (value) => {
        let d = datasetList.find((item) => item.id == value);
        if (d.problem_type == "REGRESSION") {
            setSelectedProblemType("regression");
        } else {
            setSelectedProblemType("classification");
        }
    };

    return (
        <Card title="New task">
            {status === 'loading' && <p>Loading metadata...</p>}
            {status === 'failed' && <p style={{ color: 'red' }}>Error: {error}</p>}
            {status === 'succeeded' && (
                <Form form={form} layout="vertical" onFinish={handleFinish}>
                    <Form.Item name="name" label="Name" rules={[{ required: true }]}>
                        <Input />
                    </Form.Item>

                    <Form.Item name="task_type" label="Type" rules={[{ required: true }]}>
                        <Select
                            options={[
                                { label: "Manual Train", value: "train" },
                                { label: "Hyperparameters Tuning", value: "tune" }
                            ]}
                            onChange={(val) => setSelectedTaskType(val)}
                        />
                    </Form.Item>

                    <Form.Item name="dataset_id" label="Dataset ID" rules={[{ required: true }]}>
                        <Select
                            options={datasetList.map((item) => ({
                                label: ` [${item.id.slice(-5)}] ${item.name}`, value: item.id
                            }))}
                            onChange={handleDatasetChange}
                        />
                    </Form.Item>

                    <Form.Item label="Model Name">
                        <Select placeholder="Select a model" value={selectedModelName} onChange={val => setSelectedModelName(val)}>
                            {modelNames.map(m => <Option key={m} value={m}>{m}</Option>)}
                        </Select>
                    </Form.Item>

                    {selectedTaskType === "train" && selectedModelName && selectedProblemType && (
                        <>
                            <Form.Item label="Training Hyperparameters">
                                <Form.List name="training_params">
                                    {(fields, { add, remove }) => (
                                        <>
                                            {fields.map(field => (
                                                <div style={{ display: 'flex', gap: '8px', marginBottom: '8px' }} key={field.key}>
                                                    <Form.Item
                                                        name={[field.name, 'hyperparam_name']}
                                                        rules={[{ required: true, message: 'Chọn hyperparam' }]}
                                                    >
                                                        <Select
                                                            placeholder="Hyperparameter"
                                                            options={getHyperparamOptions()}
                                                        />
                                                    </Form.Item>
                                                    <Form.Item
                                                        name={[field.name, 'value']}
                                                        rules={[{ required: true, message: 'Nhập giá trị' }]}
                                                    >
                                                        <Input placeholder="Giá trị" />
                                                    </Form.Item>
                                                    <Button type="default" danger onClick={() => remove(field.name)}>Xóa</Button>
                                                </div>
                                            ))}
                                            <Button type="dashed" onClick={() => add()}>Thêm Hyperparameter</Button>
                                        </>
                                    )}
                                </Form.List>
                            </Form.Item>
                        </>
                    )}

                    {selectedTaskType === "tune" && selectedModelName && selectedProblemType && (
                        <>
                            <Form.Item name="num_trials" label="Num Trials" rules={[{ required: true, type: 'number' }]}>
                                <InputNumber min={10} />
                            </Form.Item>
                            <Form.Item label="Tuning Hyperparameters">
                                <Form.List name="tuning_params">
                                    {(fields, { add, remove }) => (
                                        <>
                                            {fields.map(field => {
                                                const paramType = form.getFieldValue(['tuning_params', field.name, 'param_type']);

                                                return (
                                                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '8px' }} key={field.key}>
                                                        <Form.Item
                                                            name={[field.name, 'hyperparam_name']}
                                                            rules={[{ required: true, message: 'Chọn hyperparam' }]}
                                                        >
                                                            <Select
                                                                placeholder="Hyperparameter"
                                                                options={getHyperparamOptions()}
                                                            />
                                                        </Form.Item>

                                                        <Form.Item
                                                            name={[field.name, 'param_type']}
                                                            rules={[{ required: true, message: 'Chọn loại param' }]}
                                                        >
                                                            <Select
                                                                placeholder="int/float/choice"
                                                                options={[
                                                                    { label: 'int', value: 'int' },
                                                                    { label: 'float', value: 'float' },
                                                                    { label: 'choice', value: 'choice' }
                                                                ]}
                                                            />
                                                        </Form.Item>

                                                        {paramType === 'int' || paramType === 'float' ? (
                                                            <>
                                                                <Form.Item
                                                                    name={[field.name, 'lower']}
                                                                    rules={[{ required: true, message: 'Nhập lower bound' }]}
                                                                >
                                                                    <InputNumber placeholder="lower" />
                                                                </Form.Item>
                                                                <Form.Item
                                                                    name={[field.name, 'upper']}
                                                                    rules={[{ required: true, message: 'Nhập upper bound' }]}
                                                                >
                                                                    <InputNumber placeholder="upper" />
                                                                </Form.Item>
                                                            </>
                                                        ) : null}

                                                        {paramType === 'choice' ? (
                                                            <Form.Item
                                                                name={[field.name, 'choices']}
                                                                rules={[{ required: true, message: 'Nhập các lựa chọn, cách nhau bằng ;' }]}
                                                            >
                                                                <Input placeholder="value1;value2;value3" />
                                                            </Form.Item>
                                                        ) : null}

                                                        <Button type="default" danger onClick={() => remove(field.name)}>Xóa</Button>
                                                    </div>
                                                );
                                            })}
                                            <Button type="dashed" onClick={() => add()}>Thêm Hyperparameter</Button>
                                        </>
                                    )}
                                </Form.List>
                            </Form.Item>
                        </>
                    )}

                    <div style={{ marginBottom: '16px' }}>
                        <Switch checkedChildren="Scheduled" unCheckedChildren="Manual" onChange={() => setIsUseCron(!isUseCron)} />
                    </div>

                    {isUseCron && (
                        <Cron value={cronValue} setValue={setCronValue} />
                    )}

                    <Button type="primary" htmlType="submit" loading={createTaskStatus === 'loading'}>
                        Create task
                    </Button>
                </Form>
            )
            }
        </Card >
    )
};
export default TaskCreationPage;