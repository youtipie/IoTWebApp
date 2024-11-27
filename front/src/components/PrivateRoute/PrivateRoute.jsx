import { Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { selectIsLoggedIn, selectUserDataIsRefreshing } from '../../redux/auth/selectors';

const PrivateRoute = ({ component }) => {
    const isLoggedIn = useSelector(selectIsLoggedIn);
    const isRefreshing = useSelector(selectUserDataIsRefreshing);

    if (isRefreshing) {
        return <p>Loading...</p>; // Завантаження під час перевірки
    }

    return isLoggedIn ? component : <Navigate to="/login" />;
};

export default PrivateRoute;
