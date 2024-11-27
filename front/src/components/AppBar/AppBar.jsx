import module from "./AppBar.module.css"

import { useSelector } from "react-redux";
import UserMenu from "../UserMenu/UserMenu";
import AuthNav from "../AuthNav/AuthNav";
import { selectIsLoggedIn } from "../../redux/auth/selectors";
import Navigation from "../Navigation/Navigation";

const AppBar = () => {
    const isLoggedIn = useSelector(selectIsLoggedIn);

    return (
        <header className={module.header}>
            <Navigation />
            {isLoggedIn ? <UserMenu /> : <AuthNav />}
        </header>
    );
}

export default AppBar