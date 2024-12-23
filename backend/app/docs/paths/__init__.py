from .auth import spec as auth_spec
from .profile import spec as profile_spec
from .networks import spec as networks_spec
from .device import spec as device_spec

spec = {
    **auth_spec,
    **profile_spec,
    **networks_spec,
    **device_spec
}
