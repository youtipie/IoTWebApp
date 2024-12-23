spec = {
    "get": {
        "summary": "Get device subscriptions",
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
                            "subscriptions": [
                                {
                                    "actions": [
                                        {
                                            "name": "brightness",
                                            "value": 20
                                        }
                                    ],
                                    "id": "6bb38275-000a-4002-ae40-468afe936d9c",
                                    "instructions": [
                                        {
                                            "device": 3,
                                            "name": "humidity",
                                            "operator": "<",
                                            "value": 0
                                        }
                                    ],
                                    "match": "any"
                                }
                            ],
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
    },
    "post": {
        "summary": "Add instructions to device",
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
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "config": {
                                "type": "dict",
                                "description": "Control config"
                            }
                        },
                        "example": {
                            "config": {
                                "match": "any",
                                "instructions": [
                                    {
                                        "device": 4,
                                        "name": "humidity",
                                        "operator": "<",
                                        "value": 0
                                    }
                                ],
                                "actions": [
                                    {
                                        "name": "brightness",
                                        "value": 20
                                    }
                                ]
                            }
                        }
                    }
                }
            }
        },
        "responses": {
            "200": {
                "description": "Success",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "Successfully subscribed"
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
