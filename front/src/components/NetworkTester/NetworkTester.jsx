import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
    fetchNetworks,
    createNetwork,
    deleteNetwork,
    updateNetworkName,
} from "../../redux/networks/operations";
import {
    selectNetworks,
    selectIsLoadingNetworks,
    selectNetworksError,
} from "../../redux/networks/selectors";

const NetworkTester = () => {
    const dispatch = useDispatch();
    const networks = useSelector(selectNetworks);
    const isLoading = useSelector(selectIsLoadingNetworks);
    const error = useSelector(selectNetworksError);

    const [newNetworkName, setNewNetworkName] = useState("");
    const [networkNameToDelete, setNetworkNameToDelete] = useState("");
    const [networkIdToUpdate, setNetworkIdToUpdate] = useState("");
    const [newNameForUpdate, setNewNameForUpdate] = useState("");
    const [deleteError, setDeleteError] = useState(null);
    const [updateError, setUpdateError] = useState(null);

    const handleFetchNetworks = () => {
        dispatch(fetchNetworks());
    };

    const handleAddNetwork = async () => {
        if (newNetworkName.trim()) {
            try {
                const response = await dispatch(createNetwork({ name: newNetworkName })).unwrap();
                console.log("Network added successfully:", response);
                setNewNetworkName("");
                dispatch(fetchNetworks());
            } catch (err) {
                console.error("Add Network Error:", err);
            }
        }
    };

    const handleDeleteNetwork = async () => {
        if (networkNameToDelete) {
            const networkToDelete = networks.find(network => network.name === networkNameToDelete);
            if (networkToDelete) {
                try {
                    await dispatch(deleteNetwork(networkToDelete.id)).unwrap();
                    setNetworkNameToDelete("");
                    dispatch(fetchNetworks());
                } catch (err) {
                    console.error("Delete Network Error:", err);
                    setDeleteError(err.message || "Failed to delete network.");
                }
            } else {
                setDeleteError("Network with this name not found.");
            }
        }
    };

    const handleUpdateNetworkName = async () => {
        if (networkIdToUpdate && newNameForUpdate.trim()) {
            try {
                await dispatch(updateNetworkName({ id: networkIdToUpdate, name: newNameForUpdate })).unwrap();
                setNetworkIdToUpdate("");
                setNewNameForUpdate("");
                dispatch(fetchNetworks());
            } catch (err) {
                console.error("Update Network Name Error:", err);
                setUpdateError(err.message || "Failed to update network name.");
            }
        }
    };

    return (
        <div>
            <h1>Network Tester</h1>
            {isLoading && <p>Loading...</p>}
            {error && <p style={{ color: "red" }}>{error}</p>}
            {deleteError && <p style={{ color: "red" }}>{deleteError}</p>}
            {updateError && <p style={{ color: "red" }}>{updateError}</p>} {/* Виведення помилки при оновленні назви */}

            <div>
                <button onClick={handleFetchNetworks}>Fetch Networks</button>

                <div>
                    <input
                        type="text"
                        value={newNetworkName}
                        onChange={(e) => setNewNetworkName(e.target.value)}
                        placeholder="New Network Name"
                    />
                    <button onClick={handleAddNetwork}>Add Network</button>
                </div>

                <div>
                    <input
                        type="text"
                        value={networkNameToDelete}
                        onChange={(e) => setNetworkNameToDelete(e.target.value)}
                        placeholder="Network Name to Delete"
                    />
                    <button onClick={handleDeleteNetwork}>Delete Network</button>
                </div>

                <div>
                    <input
                        type="text"
                        value={networkIdToUpdate}
                        onChange={(e) => setNetworkIdToUpdate(e.target.value)}
                        placeholder="Network ID to Update"
                    />
                    <input
                        type="text"
                        value={newNameForUpdate}
                        onChange={(e) => setNewNameForUpdate(e.target.value)}
                        placeholder="New Name for Network"
                    />
                    <button onClick={handleUpdateNetworkName}>Update Network Name</button>
                </div>
            </div>

            <ul>
                {Array.isArray(networks) &&
                    networks.map((network) => (
                        <li key={network.id}>
                            {network.id}: {network.name}
                        </li>
                    ))}
            </ul>
        </div>
    );
};

export default NetworkTester;
