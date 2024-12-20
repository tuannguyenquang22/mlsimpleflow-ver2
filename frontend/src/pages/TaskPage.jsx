import { Button, Card, Table } from 'antd';
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { fetchAllTasksAsync, runTaskAsync } from '../features/model/modelSlice';
import { formatTimestamp } from "../utils/dateUtils";
import { Icon } from "@iconify/react";



function TaskPage() {
    const { taskList, taskListStatus, error, runTaskStatus, runTaskError } = useSelector(state => state.model);
    const dispatch = useDispatch();
    const navigate = useNavigate();

    useEffect(() => {
        dispatch(fetchAllTasksAsync()).unwrap().then(() => {
            console.log("Fetch tasks successfully");
        }).catch((err) => {
            console.log("Failed when fetch tasks");
        })
    }, [dispatch]);

    const handleRunTask = (taskId) => {
        dispatch(runTaskAsync(taskId)).unwrap().then(() => {
            message.success("Run task successfully and notify to you when it done.");
        }).catch((err) => {
            console.log("Failed when run task");
        });
    };

    const columns = [
        { title: 'ID', dataIndex: 'key', key: 'key', render: (text) => text.slice(-6) },
        { title: 'Name', dataIndex: 'name', key: 'name' },
        { title: 'Modified At', dataIndex: 'modified_at', key: 'modified_at' },
        { title: "Task Type", dataIndex: "task_type", key: "task_type", render: (text) => text.toUpperCase() },
        { title: "Schedule", dataIndex: "schedule", key: "schedule" },
        { title: "Action", key: "action", render: (_, record) => (
            <Button type='text' onClick={() => handleRunTask(record.key)} icon={<Icon icon="mynaui:play-solid" />} />
        )}
    ];

    const dataSource = [];
    if (taskList) {
        taskList.forEach((task) => {
            dataSource.push({
                key: task.id,
                name: task.name,
                modified_at: formatTimestamp(task.modified_at),
                task_type: task.task_type,
                schedule: task.cron_expression ? task.cron_expression : "Not scheduled"
            });
        });
    }



    return (
        <>
            <Card 
                title="Tasks"
                extra={<Button type="primary" onClick={() => navigate('/task/new')}>Create Task</Button>}
            >
                {console.log(taskList)}
                <Table columns={columns} dataSource={dataSource} />
            </Card>
        </>
    )
};

export default TaskPage;