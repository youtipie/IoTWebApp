spec = {
    "get": {
        "summary": "Get device data",
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
                            "state": {
                                "brightness": 48.389545573532516,
                                "is_enabled": True
                            },
                            "success": True
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
