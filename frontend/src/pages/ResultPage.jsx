import { Button, Card, Flex, Modal, Space, Table, Tag } from "antd";
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { fetchAllResultsAsync } from '../features/model/modelSlice';
import { formatTimestamp } from "../utils/dateUtils";
import {
    CheckCircleOutlined,
    ClockCircleOutlined,
    CloseCircleOutlined,
    ExclamationCircleOutlined,
    MinusCircleOutlined,
    SyncOutlined,
} from '@ant-design/icons';
import ConfusionMatrixChart from "../components/chart/ConfusionMatrixChart";
import TuneHistoryChart from "../components/chart/TuneHistoryChart";


function ResultPage() {
    const { resultList, resultListStatus, error } = useSelector(state => state.model);
    const dispatch = useDispatch();
    const [openDetail, setOpenDetail] = useState(false);
    const [selectedResult, setSelectedResult] = useState(null);

    useEffect(() => {
        dispatch(fetchAllResultsAsync()).unwrap().then(() => {
            console.log("Fetch results successfully");
        }).catch((err) => {
            console.log("Failed when fetch results");
        })
    }, [dispatch]);

    const handleSelectResult = (id) => {
        const result = resultList.find((r) => r.id === id);
        if (result) {
            setSelectedResult({ ...result, score_report: JSON.parse(result.score_report) });
            setOpenDetail(true);
        }
    };

    const columns = [
        { title: 'ID', dataIndex: 'key', key: 'key', render: (text) => text.slice(-6) },
        {
            title: 'Status', dataIndex: 'status', key: 'status', render: (text) => (
                <span>
                    {text === "PENDING" && (<Tag icon={<SyncOutlined spin />} color="processing">Pending</Tag>)}
                    {text === "COMPLETED" && (<Tag icon={<CheckCircleOutlined />} color="success">Success</Tag>)}
                    {text === "FAILED" && (<Tag icon={<CloseCircleOutlined />} color="error">Failure</Tag>)}
                </span>
            )
        },
        { title: 'Created At', dataIndex: 'created_at', key: 'created_at' },
        { title: 'Completed At', dataIndex: 'completed_at', key: 'completed_at' },
        { title: "Task ID", dataIndex: "task_id", key: "task_id", render: (text) => text.slice(-6) },
        {
            title: "Action", key: "action", render: (_, record) => (
                <Space>
                    {record.status === "COMPLETED" && (
                        <Button type='text' icon={<CheckCircleOutlined />} onClick={() => handleSelectResult(record.key)} />
                    )}
                </Space>
            )
        }
    ];

    const dataSource = [];
    if (resultList) {
        resultList.forEach((result) => {
            dataSource.push({
                key: result.id,
                status: result.status,
                created_at: formatTimestamp(result.created_at),
                completed_at: result.completed_at ? formatTimestamp(result.completed_at) : "...Waiting",
                task_id: result.task_id
            });
        });
    }

    return (
        <>
            <Modal
                title="Result Detail"
                open={openDetail}
                width={1200}
                onCancel={() => setOpenDetail(false)}
                footer={null}
            >
                {selectedResult && (
                    <>
                        {console.log(selectedResult)}
                        <p>Task ID: {selectedResult.task_id}</p>
                        <p>Task Type: {selectedResult.task_type}</p>
                        <p>Status: {selectedResult.status}</p>
                        <p>Created At: {formatTimestamp(selectedResult.created_at)}</p>
                        <p>Completed At: {selectedResult.completed_at ? formatTimestamp(selectedResult.completed_at) : "...Waiting"}</p>
                        {selectedResult.task_type === "tune" && (
                            <>
                                <p>Score Report: best {selectedResult.score_report.metric} is {selectedResult.score_report.best_score}</p>
                                <div style={{ marginBottom: 20 }}>
                                    <ConfusionMatrixChart target_true={selectedResult.target_true} target_pred={selectedResult.target_pred} />
                                </div>
                                <div style={{ marginBottom: 20 }}>
                                    <TuneHistoryChart history={selectedResult.score_report.history} />
                                </div>
                            </>
                        )}
                    </>
                )}
            </Modal>
            <Card title="Result">
                <Table columns={columns} dataSource={dataSource} />
            </Card>
        </>
    )
};

export default ResultPage;