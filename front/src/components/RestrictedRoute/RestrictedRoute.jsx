import { Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { selectIsLoggedIn, selectUserDataIsRefreshing } from '../../redux/auth/selectors';

const RestrictedRoute = ({ component }) => {
    const isLoggedIn = useSelector(selectIsLoggedIn);
    const isRefreshing = useSelector(selectUserDataIsRefreshing);

    if (isRefreshing) {
        return <p>Loading...</p>;
    }

    return isLoggedIn ? <Navigate to="/" /> : component;
};

export default RestrictedRoute;
