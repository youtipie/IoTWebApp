import module from "./Navigation.module.css"

import { useSelector } from "react-redux";
import { selectIsLoggedIn } from "../../redux/auth/selectors";
import { NavLink } from "react-router-dom";
import clsx from "clsx";

const buildCssClasses = ({ isActive }) => clsx(module.link, isActive && module.active);

const Navigation = () => {
    const isLoggedIn = useSelector(selectIsLoggedIn);

    return (
        <div className={module.navigation}>
            <NavLink className={buildCssClasses} to="/">Home</NavLink>
            {isLoggedIn && (
                <NavLink className={buildCssClasses} to="/device-list">Devices</NavLink>
            )}
        </div>
    );
}

export default Navigation   