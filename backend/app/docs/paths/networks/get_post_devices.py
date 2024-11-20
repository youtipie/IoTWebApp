spec = {
    "get": {
        "summary": "Get devices in specified network",
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
                "description": "Devices in network",
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "id": 5,
                                "ip": "127.0.0.1",
                                "name": "Device",
                                "port": 1234
                            },
                            {
                                "id": 7,
                                "ip": "127.0.0.1",
                                "name": "Device1",
                                "port": 1236
                            }
                        ]
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
    },
    "post": {
        "summary": "Add new device to network",
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
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "ip": {
                                "type": "string",
                                "description": "ipv4 or ipv6 of device"
                            },
                            "port": {
                                "type": "integer",
                                "description": "Int number in range [0, 65535]"
                            },
                            "name": {
                                "type": "string"
                            }
                        },
                        "example": {
                            "ip": "127.0.0.1",
                            "port": 1234,
                            "name": "Device"
                        }
                    }
                }
            }
        },
        "responses": {
            "200": {
                "description": "Newly added device",
                "content": {
                    "application/json": {
                        "example": {
                            "id": 5,
                            "ip": "127.0.0.1",
                            "name": "Device",
                            "port": 1234
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
