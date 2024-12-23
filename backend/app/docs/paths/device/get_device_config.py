spec = {
    "get": {
        "summary": "Get device config",
        "tags": [
            "Device"
        ],
        "parameters": [
            {
                "in": "path",
                "name": "device_id",
                "schema": {
                    "type": "integer"
                },
                "required": True,
                "description": "Numeric ID of the device"
            }
        ],
        "responses": {
            "200": {
                "description": "Successful request",
                "content": {
                    "application/json": {
                        "example": {
                            "id": 3,
                            "name": "Temp1",
                            "parameters": {
                                "brightness": {
                                    "max": 50,
                                    "min": -50,
                                    "type": "range"
                                }
                            },
                            "readings": {
                                "is_enabled": {
                                    "default": False,
                                    "type": "bool"
                                }
                            }
                        }
                    }
                }
            },
            "401": {
                "$ref": "#/components/responses/UnauthorizedError"
            },
            "404": {
                "$ref": "#/components/responses/User404"
            }
        }
    }
}
