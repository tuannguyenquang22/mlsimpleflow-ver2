import { Card, Col, Row, Space } from 'antd';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Icon } from "@iconify/react";


function LandingPage() {
    const navigate = useNavigate();

    return (
        <div>
            <h1>Welcome to the Simpleflow</h1>
            <p>We provide a range of features designed to simplify and streamline processes in machine learning model development. SimpleFlow empowers you to focus on building robust models with ease.</p>
            <Row gutter={16} style={{ marginTop: 16 }}>
                <Col span={6}>
                    <Card style={{ height: "100%"}} hoverable onClick={() => navigate('/dataset/upload')}>
                        <Space>
                            <Icon icon="material-symbols:upload" width="40" height="40" />
                            <h3>Upload Raw Dataset</h3>
                        </Space>
                        <p>Easily upload your raw datasets (csv files) to kickstart your machine learning workflow.</p>
                    </Card>
                </Col>
                <Col span={6}>
                    <Card style={{ height: "100%"}} hoverable onClick={() => navigate('/dataset/raw')}>
                        <Space>
                            <Icon icon="ion:hammer-sharp" width="40" height="40" />
                            <h3>Auto Preprocessing</h3>
                        </Space>
                        <p>Automatically preprocess your dataset to save time and effort.</p>
                    </Card>
                </Col>
                <Col span={6}>
                    <Card style={{ height: "100%"}} hoverable onClick={() => navigate('/task/new')}>
                        <Space>
                            <Icon icon="octicon:ai-model-16" width="40" height="40" />
                            <h3>Model Training</h3>
                        </Space>
                        <p>Setup a simply task for training model on preprocessed dataset by manual or scheduling.</p>
                    </Card>
                </Col>
                <Col span={6}>
                    <Card style={{ height: "100%"}} hoverable onClick={() => navigate('/task/new')}>
                        <Space>
                            <Icon icon="material-symbols:tune" width="40" height="40" />
                            <h3>Model Tuning</h3>
                        </Space>
                        <p>Setup a simply task for tuning model hyperparameters on preprocessed dataset by manual or scheduling.</p>
                    </Card>
                </Col>
            </Row>
        </div>
    )
}

export default LandingPage;
