from .paths import spec as path_spec
from .components import spec as components_spec

# Using spec as dict instead of yaml, because flasgger is piece of shit
spec = {
    "info": {
        "title": "IoT Device Manager",
        "description": "API for managing a IoT devices",
        "version": "1.0"
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
