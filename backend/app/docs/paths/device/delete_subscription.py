spec = {
    "delete": {
        "summary": "Unsubscribe device from other device",
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
            },
            {
                "in": "path",
                "name": "subscription_id",
                "schema": {
                    "type": "string"
                },
                "required": True,
                "description": "String id of the device subscription"
            }
        ],
        "responses": {
            "200": {
                "description": "Success",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "Successfully unsubscribed"
                        }
                    }
                }
            },
            "400": {
                "$ref": "#/components/responses/BadValues"
            },
            "401": {
                "$ref": "#/components/responses/UnauthorizedError"
            },
            "404": {
                "$ref": "#/components/responses/User404"
            },
            "500": {
                "$ref": "#/components/responses/500"
            }
        }
    }
}
