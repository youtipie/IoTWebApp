from .get_post_network import spec as networks_spec
from .put_delete_network import spec as put_delete_spec
from .users_in_network import spec as users_network_spec
from .user_network import spec as user_network
from .quit_network import spec as quit_network
from .get_post_devices import spec as get_devices
from .delete_device import spec as delete_device

spec = {
    "/networks": networks_spec,
    "/networks/{network_id}": put_delete_spec,
    "/networks/{network_id}/users": users_network_spec,
    "/networks/{network_id}/users/{user_id}": user_network,
    "/networks/{network_id}/quit": quit_network,
    "/networks/{network_id}/devices": get_devices,
    "/networks/{network_id}/devices/{device_id}": delete_device,
}
