spec = {
    "get": {
        "summary": "User profile",
        "tags": [
            "Profile"
        ],
        "responses": {
            "200": {
                "description": "User profile",
                "content": {
                    "application/json": {
                        "$ref": "#components/examples/User"
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
    "delete": {
        "summary": "Delete user profile",
        "tags": [
            "Profile"
        ],
        "responses": {
            "200": {
                "description": "User profile",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "User deleted successfully."
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
