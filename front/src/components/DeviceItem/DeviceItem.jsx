import module from "./DeviceItem.module.css";
import { Link } from 'react-router-dom';

const DeviceItem = ({ device }) => {
    const statusColor = device.status === 'Active' ? 'green' : 'red';

    return (
        <li className={module.deviceItem}>
            <Link className={module.deviceLink} to={`/device/${device.id}`}>
                {device.name} State: <span style={{ color: statusColor }}>{device.status}</span>
            </Link>
        </li>
    );
};

export default DeviceItem;
