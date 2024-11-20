import { NavLink } from "react-router-dom";
import module from "./AuthNav.module.css";
import clsx from "clsx";

const buildCssClasses = ({ isActive }) => clsx(module.link, isActive && module.active);

const AuthNav = () => {
    return (
        <div className={module.linkDiv}>
            <NavLink className={buildCssClasses} to="/register">Sign Up</NavLink>
            <NavLink className={buildCssClasses} to="/login">Log in</NavLink>
        </div>
    );
};

export default AuthNav