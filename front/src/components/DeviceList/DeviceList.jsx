import module from "./DeviceList.module.css";
import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchDevices } from "../../redux/devices/operations";
import { selectDevices, selectIsLoadingDevices, selectDevicesError } from "../../redux/devices/selectors";
import DeviceItem from "../DeviceItem/DeviceItem";

const DeviceList = ({ networkId }) => {
    const dispatch = useDispatch();
    const devices = useSelector(selectDevices);
    const isLoading = useSelector(selectIsLoadingDevices);
    const error = useSelector(selectDevicesError);

    useEffect(() => {
        if (networkId) {
            dispatch(fetchDevices(networkId));
        }
    }, [dispatch, networkId]);

    return (
        <div>
            {isLoading && <p>Loading devices...</p>}
            {error && <p className={module.error}>{error}</p>}
            <ul className={module.deviceList}>
                {devices.map((device) => (
                    <DeviceItem key={device.id} device={device} />
                ))}
            </ul>
        </div>
    );
};

export default DeviceList;
