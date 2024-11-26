import module from "./UserMenu.module.css"

import { useDispatch } from "react-redux";
import { logout } from "../../redux/auth/operations";
// import { selectUser } from "../../redux/auth/selectors";

const UserMenu = () => {
    const dispatch = useDispatch();
    // const user = useSelector(selectUser);

    const handleClick = () => {
        dispatch(logout());
    }

    return (
        <div className={module.userDiv}>
            <p className={module.userName}>Your Office</p>
            <button className={module.button} type="button" onClick={handleClick}>Log out</button>
        </div>
    );
};

export default UserMenu