from .get_device_state import spec as get_device_state_spec
from .get_device_config import spec as get_device_config_spec
from .get_post_subscription import spec as get_post_subscription
from .delete_subscription import spec as delete_subscription_spec

spec = {
    "/device/{device_id}/state": get_device_state_spec,
    "/device/{device_id}/config": get_device_config_spec,
    "/device/{device_id}/subscriptions": get_post_subscription,
    "/device/{device_id}/subscriptions/{subscription_id}": delete_subscription_spec,
}
