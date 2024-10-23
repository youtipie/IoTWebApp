import module from "./HomePage.module.css"

import { useNavigate } from 'react-router-dom';
import DeviceList from '../../components/DeviceList/DeviceList';

const HomePage = () => {

    const navigate = useNavigate();

    const handleAddDevice = () => {
        navigate('/create-device'); // Перехід на сторінку створення девайсу
    };

    return (
        <div className={module.homeDiv}>
            <h1 className={module.header}>Мої девайси</h1>
            <DeviceList />
            <button className={module.addBtn} onClick={handleAddDevice}>Додати новий девайс</button>
        </div>
    );
};

export default HomePage;
