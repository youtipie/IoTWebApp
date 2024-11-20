spec = {
    "delete": {
        "summary": "Delete device from network",
        "tags": [
            "Network"
        ],
        "parameters": [
            {
                "in": "path",
                "name": "network_id",
                "schema": {
                    "type": "integer"
                },
                "required": True,
                "description": "Numeric ID of the network"
            },
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
                "description": "Successful deletion",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "Successfully deleted"
                        }
                    }
                }
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
