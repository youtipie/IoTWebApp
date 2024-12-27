import module from "./DeviceItem.module.css";
import { Link } from 'react-router-dom';

const DeviceItem = ({ device, network }) => {
    const statusColor = device.status === 'Active' ? 'green' : 'red';

    return (
        <li className={module.deviceItem}>
            <Link className={module.deviceLink} to={`/device/${device.id}`}>
                <div>
                    <strong>{device.name}</strong>
                    <p>
                        State: <span style={{ color: statusColor }}>{device.status}</span>
                    </p>
                    <p>
                        Network: <span>{network?.name || 'Unknown'}</span>
                    </p>
                </div>
            </Link>
        </li>
    );
};

export default DeviceItem;
