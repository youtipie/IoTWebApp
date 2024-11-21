spec = {
    "post": {
        "summary": "Login user",
        "description": "Login user using email and password",
        "tags": [
            "Auth"
        ],
        "security": [],
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
                            "password": {
                                "type": "string"
                            }
                        },
                        "example": {
                            "email": "user@gmail.com",
                            "password": "verySecured8CharPass"
                        }
                    }
                }
            }
        },
        "responses": {
            "200": {
                "description": "Successfully authenticated. The access token and refresh token are returned. "
                               "You need to include access token in subsequent requests. "
                               "Refresh token can be used to refresh current user's access token after it expires.",
                "content": {
                    "application/json": {
                        "example": {
                            "access_token": "aaaaaaa.bbbbbbbb.ccccccc",
                            "refresh_token": "aaaaaaaaaaa.bbbbbbbbbbb.ccccccccc",
                        }
                    }
                }
            },
            "400": {
                "$ref": "#/components/responses/BadValues"
            },
            "401": {
                "description": "Invalid credentials",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "Invalid email or password."
                        }
                    }
                }
            }
        }
    }
}
