spec = {
    "get": {
        "summary": "Get users in specified network",
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
                "description": "Users in network",
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "email": "user1@gmail.com",
                                "id": 1,
                                "rights": "a",
                                "username": "user1"
                            },
                            {
                                "email": "user@gmail.com",
                                "id": 4,
                                "rights": "w",
                                "username": "user"
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
        "summary": "Add user to network",
        "description": "Specified user will receive email with invitation",
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
                            "email": {
                                "type": "string"
                            },
                            "rights": {
                                "type": "string",
                                "description": "Single number that describe user rights:  w, r"
                            }
                        },
                        "example": {
                            "email": "user@gmail.com",
                            "rights": "w"
                        }
                    }
                }
            }
        },
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
                "description": "Successful operation",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "Successfully added user to your network"
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
    },
}
