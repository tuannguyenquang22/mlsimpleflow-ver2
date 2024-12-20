import { useSelector } from 'react-redux';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
    const { access_token } = useSelector(state => state.auth);
    if (!access_token) {
        return <Navigate to="/login" replace />;
    }
    return children;
};

export default ProtectedRoute;