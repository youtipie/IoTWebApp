spec = {
    "put": {
        "summary": "Update name of user network",
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
                "description": "Updated network",
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
            "403": {
                "description": "User that don't own the network, cannot change it's name",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "You cannot rename this network."
                        }
                    }
                }
            },
            "404": {
                "$ref": "#/components/responses/User404"
            }
        }
    },
    "delete": {
        "summary": "Delete network",
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
                "description": "Successful deletion of network",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "Successfully deleted network"
                        }
                    }
                }
            },
            "401": {
                "$ref": "#/components/responses/UnauthorizedError"
            },
            "403": {
                "description": "User that don't own the network, cannot change it's name",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "You cannot rename this network."
                        }
                    }
                }
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
