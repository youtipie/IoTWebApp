spec = {
    "post": {
        "summary": "Quit from specified network",
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
            }
        ],
        "responses": {
            "200": {
                "description": "Successful quit",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "Successfully quit network"
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
