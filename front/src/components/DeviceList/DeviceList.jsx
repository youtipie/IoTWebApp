import module from "./DeviceList.module.css"

import { useEffect, useState } from 'react';
import DeviceItem from '../DeviceItem/DeviceItem';

const DeviceList = () => {
    const [devices, setDevices] = useState([]);

    useEffect(() => {
        const fetchedDevices = [
            { id: 1, name: 'Thermostat', status: 'Active' },
            { id: 2, name: 'Camera', status: 'Inactive' },
        ];
        setDevices(fetchedDevices);
    }, []);

    return (
        <ul className={module.deviceList}>
            {devices.map((device) => (
                <DeviceItem key={device.id} device={device} />
            ))}
        </ul>
    );
};

export default DeviceList;
