import DeviceList from "../../components/DeviceList/DeviceList";
import module from "./DeviceListPage.module.css"

import { useNavigate } from "react-router-dom";

const DeviceListPage = () => {
    const navigate = useNavigate();

    const handleAddDevice = () => {
        navigate('/create-device'); // Перехід на сторінку створення девайсу
    };

    return (
        <div className={module.homeDiv}>
            <h1 className={module.header}>Мої девайси</h1>
            <DeviceList />
            <button className={module.addBtn} onClick={handleAddDevice}>Підключити новий девайс</button>
        </div>
    );
}

export default DeviceListPage