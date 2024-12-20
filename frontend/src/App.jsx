import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Button, Flex, Layout, Menu } from 'antd';
import { useSelector, useDispatch } from 'react-redux';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import PreprocessingPage from './pages/PreprocessingPage';
import ProtectedRoute from './components/ProtectedRoute';
import { logout } from './features/auth/authSlice';
import DatasetRawPage from './pages/DatasetRawPage';
import LandingPage from './pages/LandingPage';
import DatasetUploadPage from './pages/DatasetUploadPage';
import DatasetPreprocessedPage from './pages/DatasetPreprocessedPage';
import TaskCreationPage from './pages/TaskCreationPage';
import TaskPage from './pages/TaskPage';
import ResultPage from './pages/ResultPage';

const { Header, Content } = Layout;

function App() {
    const { access_token } = useSelector(state => state.auth);
    const dispatch = useDispatch();

    const handleLogout = () => {
        dispatch(logout());
    };

    const menuItemsOS = [
        { key: "login", label: <Link to="/login">Login</Link> },
        { key: "register", label: <Link to="/register">Register</Link> }
    ];

    const menuItemsIS = [
        { key: "home", label: <Link to="/">Home</Link> },
        { key: "raw", label: <Link to="/dataset/raw">Raw Dataset</Link> },
        { key: "prep", label: <Link to="/dataset/preprocessed">Preproccessed Dataset</Link> },
        { key: "task", label: <Link to="/task">Task</Link> },
        { key: "result", label: <Link to="/result">Result</Link> },
    ]

    return (
        <Router>
            <Layout>
                <Header>
                    <Flex
                        align='center'
                    >
                        <Menu
                            theme="dark"
                            mode="horizontal"
                            items={access_token ? menuItemsIS : menuItemsOS}
                            style={{ width: "100%" }}
                        />
                        {access_token && (
                            <Button onClick={handleLogout}>Logout</Button>
                        )}
                    </Flex>
                </Header>
                <Content style={{ padding: '20px' }}>
                    <Routes>
                        <Route path="/login" element={<LoginPage />} />
                        <Route path="/register" element={<RegisterPage />} />
                        <Route path="/" element={
                            <ProtectedRoute>
                                <LandingPage />
                            </ProtectedRoute>
                        } />
                        <Route path="/preprocess/:dataset_id" element={
                            <ProtectedRoute>
                                <PreprocessingPage />
                            </ProtectedRoute>
                        } />
                        <Route path="/dataset/raw" element={
                            <ProtectedRoute>
                                <DatasetRawPage />
                            </ProtectedRoute>
                        } />
                        <Route path="/dataset/preprocessed" element={
                            <ProtectedRoute>
                                <DatasetPreprocessedPage />
                            </ProtectedRoute>
                        } />
                        <Route path="/dataset/upload" element={
                            <ProtectedRoute>
                                <DatasetUploadPage />
                            </ProtectedRoute>
                        } />
                        <Route path="/task" element={
                            <ProtectedRoute>
                                <TaskPage />
                            </ProtectedRoute>
                        } />
                        <Route path="/task/new" element={
                            <ProtectedRoute>
                                <TaskCreationPage />
                            </ProtectedRoute>
                        } />
                        <Route path="/result" element={
                            <ProtectedRoute>
                                <ResultPage />
                            </ProtectedRoute>
                        } />
                    </Routes>
                </Content>
            </Layout>
        </Router>
    );
}

export default App;
