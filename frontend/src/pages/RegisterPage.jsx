import React, { useState } from 'react';
import { Form, Input, Button, Card } from 'antd';
import { useDispatch } from 'react-redux';
import { registerAsync } from '../features/auth/authSlice';
import { useNavigate } from 'react-router-dom';

function RegisterPage() {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);

    const onFinish = (values) => {
        setLoading(true);
        dispatch(registerAsync(values))
            .unwrap()
            .then(() => {
                navigate('/login');
            })
            .finally(() => setLoading(false));
    };

    return (
        <Card title="Đăng ký" style={{ width: 300, margin: '50px auto' }}>
            <Form onFinish={onFinish} layout="vertical">
                <Form.Item name="display_name" label="Tên hiển thị" rules={[{ required: true }]}>
                    <Input />
                </Form.Item>
                <Form.Item name="email" label="Email" rules={[{ required: true, type: 'email' }]}>
                    <Input />
                </Form.Item>
                <Form.Item name="password" label="Mật khẩu" rules={[{ required: true }]}>
                    <Input.Password />
                </Form.Item>
                <Button type="primary" htmlType="submit" loading={loading}>Đăng ký</Button>
            </Form>
        </Card>
    );
}

export default RegisterPage;
