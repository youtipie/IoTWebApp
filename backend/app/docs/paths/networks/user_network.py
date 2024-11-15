spec = {
    "put": {
        "summary": "Change rights of specified user",
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
                "name": "user_id",
                "schema": {
                    "type": "integer"
                },
                "required": True,
                "description": "Numeric ID of the user"
            }
        ],
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "rights": {
                                "type": "string",
                                "description": "Single number that describe user rights:  w, r"
                            }
                        },
                        "example": {
                            "rights": "w"
                        }
                    }
                }
            }
        },
        "responses": {
            "200": {
                "description": "Successful change",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "Successfully changed user rights"
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
            "403": {
                "$ref": "#/components/responses/NotAdmin"
            },
            "404": {
                "$ref": "#/components/responses/User404"
            },
            "500": {
                "$ref": "#/components/responses/500"
            }
        }
    },
    "delete": {
        "summary": "Delete user from network",
        "description": "Specified user will receive email with invitation",
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
                "name": "user_id",
                "schema": {
                    "type": "integer"
                },
                "required": True,
                "description": "Numeric ID of the user"
            }
        ],
        "responses": {
            "200": {
                "description": "Successful deletion",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "Successfully deleted user from your network"
                        }
                    }
                }
            },
            "401": {
                "$ref": "#/components/responses/UnauthorizedError"
            },
            "403": {
                "$ref": "#/components/responses/NotAdmin"
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
