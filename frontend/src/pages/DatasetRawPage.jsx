import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchDatasetsAsync, preprocessDatasetAsync } from '../features/dataset/datasetSlice';
import { Card, Select, Button, Table, message, Space, Modal, Input, Form, Alert } from 'antd';
import { formatTimestamp } from "../utils/dateUtils";
import { Icon } from "@iconify/react";



function DatasetRawPage() {
    const dispatch = useDispatch();
    const { datasetList, listStatus, error } = useSelector(state => state.dataset)
    const [preprocessingOpen, setPreprocessingOpen] = useState(false);
    const [chosenDataset, setChosenDataset] = useState(null);
    const [targetColumn, setTargetColumn] = useState(null);

    const datasetType = "raw";

    useEffect(() => {
        dispatch(fetchDatasetsAsync(datasetType)).unwrap().then(() => {
            console.log("Fetch raw datasets successfully");
        })
            .catch((err) => {
                message.error("Failed when fetch raw datasets");
            })
    }, [dispatch, datasetType]);

    const handleTargetColumnChange = (value) => {
        setTargetColumn(value);
    };

    const handlePreprocessing = () => {
        if (!targetColumn) {
            message.error('Target column is required');
            return;
        }
        console.log(targetColumn)
        dispatch(preprocessDatasetAsync({ dataset_id: chosenDataset.id, target_column: targetColumn }))
            .unwrap()
            .then(() => {
                message.success('Preproccessing dataset will be started soon.');
                if (preprocessingOpen) {
                    setPreprocessingOpen(false);
                }
            })
            .catch(() => {
                message.error('Unable to preprocess dataset');
            });
    };

    const columns = [
        { title: 'Name', dataIndex: 'name', key: 'name' },
        { title: 'Created At', dataIndex: 'created_at', key: 'created_at' },
        { title: "Columns", dataIndex: "columns", key: "columns" },
        { title: "Rows", dataIndex: "rows", key: "rows" },
        {
            title: "Action",
            key: "action",
            render: (_, record) => (
                <Space>
                    <Button 
                        onClick={() => {
                            let d = datasetList.find((item) => item.id === record.key)
                            setChosenDataset(d);
                            setPreprocessingOpen(true);
                        }} 
                        type='text'
                        icon={<Icon icon="ion:hammer-sharp" />}
                    />
                </Space>
            )
        },
    ];

    const dataSource = [];
    if (datasetList) {
        datasetList.map((item) => {
            dataSource.push({
                key: item.id,
                name: item.name,
                created_at: formatTimestamp(item.created_at),
                columns: item.columns.length,
                rows: item.num_rows
            })
        })
    }

    return (
        <>
            <Modal
                title="Preprocessing Dataset"
                open={preprocessingOpen}
                onCancel={() => setPreprocessingOpen(false)}
                width={800}
                onOk={handlePreprocessing}
            >
                {chosenDataset && (
                    <>
                        <Form layout='vertical'>
                            <Form.Item label="Name">
                                <Input value={chosenDataset.name} disabled />
                            </Form.Item>
                            <Form.Item label="Columns">
                                <Table
                                    columns={[
                                        { key: "column", title: "Name", dataIndex: "column" },
                                        { key: "data_type", title: "Data Type", dataIndex: "data_type" }
                                    ]}
                                    dataSource={chosenDataset.columns.map((_, index) => ({
                                        key: index,
                                        column: chosenDataset.columns[index],
                                        data_type: chosenDataset.data_types[index],
                                    }))}
                                    rowSelection={{}}
                                    pagination={false}
                                />
                            </Form.Item>
                            <Form.Item label="Target column">
                                <Select 
                                    options={chosenDataset.columns.map((item) => ({
                                        label: item,
                                        value: item,
                                    }))}
                                    onChange={handleTargetColumnChange}
                                />
                            </Form.Item>
                        </Form>
                    </>
                )}
            </Modal>
            <Card title="Raw Dataset">
                <Alert message="Click on the hammer icon to preprocess the dataset" type="info" showIcon style={{ marginBottom: 20 }}/>
                <Table columns={columns} dataSource={dataSource} />
            </Card>
        </>
    )
}

export default DatasetRawPage;