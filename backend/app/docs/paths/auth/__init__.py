from .register import spec as register_spec
from .login import spec as login_spec
from .refresh import spec as refresh_spec

spec = {
    "/auth/login": login_spec,
    "/auth/register": register_spec,
    "/auth/refresh": refresh_spec
}
