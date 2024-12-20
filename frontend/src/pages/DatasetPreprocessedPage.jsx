import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchDatasetsAsync } from '../features/dataset/datasetSlice';
import { Card, Select, Button, Table, message, Space } from 'antd';
import { formatTimestamp } from '../utils/dateUtils';
import { Icon } from "@iconify/react";



function DatasetPreprocessedPage() {
    const dispatch = useDispatch();
    const { datasetList, listStatus, error } = useSelector(state => state.dataset)
    const datasetType = "preprocessed";

    useEffect(() => {
        dispatch(fetchDatasetsAsync(datasetType)).unwrap().then(() => {
            message.success("Fetch raw datasets successfully");
        })
        .catch((err) => {
            message.error("Failed when fetch raw datasets");
        })
    }, [dispatch, datasetType]);

    
    const columns = [
        { title: "ID", dataIndex: "key", key: "key", render: (text) => text.slice(-6) },
        { title: 'Name', dataIndex: 'name', key: 'name'},
        { title: 'Created At', dataIndex: 'created_at', key: 'created_at' },
        { title: "Columns", dataIndex: "columns", key: "columns" },
        { title: "Rows", dataIndex: "rows", key: "rows" },
        { title: "Problem Type", dataIndex: "problem_type", key: "problem_type" },
        { title: "Target", dataIndex: "target_column", key: "target_column" },
        {
            title: "Action",
            key: "action",
            render: (_, record) => (
                <Space>
                    <Button
                        icon={<Icon icon="lets-icons:view-alt-fill" />}
                        type='text'
                    />
                    <Button
                        icon={<Icon icon="mdi:trash" />}
                        type='text'
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
                rows: item.num_rows,
                problem_type: item.problem_type,
                target_column: item.target_column,
            })
        })
    }

    return (
        <Card title="Preprocessed Dataset">
            <Table columns={columns} dataSource={dataSource} />
        </Card>
    )
}

export default DatasetPreprocessedPage;