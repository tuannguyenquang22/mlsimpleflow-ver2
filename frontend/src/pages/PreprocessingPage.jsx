import React, { useState } from 'react';
import { Card, Form, Input, Button, message } from 'antd';
import { useParams } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { preprocessDatasetAsync } from '../features/dataset/datasetSlice';

function PreprocessingPage() {
    const { dataset_id } = useParams();
    const dispatch = useDispatch();
    const [targetColumn, setTargetColumn] = useState('');

    const handlePreprocess = () => {
        if (!targetColumn) {
            message.error('Hãy nhập target_column');
            return;
        }
        dispatch(preprocessDatasetAsync({ dataset_id, target_column: targetColumn }))
            .unwrap()
            .then(() => {
                message.success('Tiền xử lý thành công!');
            })
            .catch(() => {
                message.error('Tiền xử lý thất bại!');
            });
    };

    return (
        <Card title="Tiền xử lý dataset">
            <Form layout="vertical">
                <Form.Item label="Target Column">
                    <Input value={targetColumn} onChange={(e) => setTargetColumn(e.target.value)} />
                </Form.Item>
                <Button type="primary" onClick={handlePreprocess}>Tiền xử lý</Button>
            </Form>
        </Card>
    );
}

export default PreprocessingPage;
