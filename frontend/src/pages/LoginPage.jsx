import React, { useState } from 'react';
import { Form, Input, Button, Card } from 'antd';
import { useDispatch, useSelector } from 'react-redux';
import { loginAsync } from '../features/auth/authSlice';
import { useNavigate } from 'react-router-dom';

function LoginPage() {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);

    const onFinish = (values) => {
        setLoading(true);
        dispatch(loginAsync(values))
            .unwrap()
            .then(() => {
                navigate('/');
            })
            .finally(() => setLoading(false));
    };

    return (
        <Card title="Đăng nhập" style={{ width: 300, margin: '50px auto' }}>
            <Form onFinish={onFinish} layout="vertical">
                <Form.Item name="username" label="Email / Username" rules={[{ required: true }]} >
                    <Input />
                </Form.Item>
                <Form.Item name="password" label="Mật khẩu" rules={[{ required: true }]}>
                    <Input.Password />
                </Form.Item>
                <Button type="primary" htmlType="submit" loading={loading}>Đăng nhập</Button>
            </Form>
        </Card>
    );
}

export default LoginPage;
