from .paths import spec as path_spec
from .components import spec as components_spec

# Using spec as dict instead of yaml, because flasgger is piece of shit
spec = {
    "info": {
        "title": "Bookstore API",
        "description": "API for managing a bookstore",
        "version": "0.5.0"
    },
    "basePath": "/",
    "schemes": [
        "http",
        "https"
    ],
    "paths": {
        **path_spec
    },
    "components": {
        **components_spec
    },
    "security": [
        {
            "bearerAuth": []
        },
    ]
}
