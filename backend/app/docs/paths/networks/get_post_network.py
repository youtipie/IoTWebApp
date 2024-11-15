spec = {
    "get": {
        "summary": "Get networks that include current user",
        "tags": [
            "Network"
        ],
        "responses": {
            "200": {
                "description": "User networks",
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "devices": [],
                                "id": 1,
                                "name": "Default network",
                                "rights": "a",
                                "users": [
                                    {
                                        "email": "user1@gmail.com",
                                        "id": 1,
                                        "rights": "a",
                                        "username": "user1"
                                    }
                                ]
                            },
                            {
                                "devices": [],
                                "id": 6,
                                "name": "Test network",
                                "rights": "w",
                                "users": [
                                    {
                                        "email": "user@gmail.com",
                                        "id": 2,
                                        "rights": "a",
                                        "username": "user"
                                    },
                                    {
                                        "email": "user1@gmail.com",
                                        "id": 1,
                                        "rights": "w",
                                        "username": "user1"
                                    }
                                ]
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
        "summary": "Create new network",
        "tags": [
            "Network"
        ],
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string"
                            }
                        },
                        "example": {
                            "name": "New name for my cool network",
                        }
                    }
                }
            }
        },
        "responses": {
            "200": {
                "description": "Created network",
                "content": {
                    "application/json": {
                        "$ref": "#/components/examples/Network"
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
            }
        }
    },
}
