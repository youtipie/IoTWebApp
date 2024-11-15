from .register import spec as register_spec
from .login import spec as login_spec
from .logout import spec as logout_spec

spec = {
    "/auth/login": login_spec,
    "/auth/register": register_spec,
    "/auth/logout": logout_spec
}
