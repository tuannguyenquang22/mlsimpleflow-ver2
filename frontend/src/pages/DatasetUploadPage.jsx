import React, { useState } from 'react';
import { Card, Form, Input, Button, Upload, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import { useDispatch, useSelector } from 'react-redux';
import { uploadDatasetAsync } from '../features/dataset/datasetSlice';
import { Link } from 'react-router-dom';

function DatasetUploadPage() {
    const dispatch = useDispatch();
    const [file, setFile] = useState(null);
    const { uploadedDataset, uploadStatus } = useSelector(state => state.dataset);

    const handleSubmit = () => {
        if (!file) {
            message.error('Hãy chọn file!');
            return;
        }
        dispatch(uploadDatasetAsync({ file }))
            .unwrap()
            .then(() => {
                message.success('Upload thành công!');
            })
            .catch(err => {
                message.error('Upload thất bại!');
            });
    };

    const props = {
        beforeUpload: (file) => {
            setFile(file);
            return false; // không upload tự động
        }
    };

    return (
        <Card title="Dataset Upload">
            <Form layout="vertical">
                <Form.Item label="File CSV">
                    <Upload {...props}>
                        <Button icon={<UploadOutlined />}>Chọn file CSV</Button>
                    </Upload>
                    {file && <p>Đã chọn file: {file.name}</p>}
                </Form.Item>
                <Button type="primary" onClick={handleSubmit} loading={uploadStatus === 'loading'}>
                    Upload
                </Button>
            </Form>
        </Card>
    );
}

export default DatasetUploadPage;
