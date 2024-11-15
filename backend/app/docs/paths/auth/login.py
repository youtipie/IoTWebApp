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
                "description": "Successfully authenticated. The access token is returned in a cookie named `access_token_cookie`. "
                               "You need to include this cookie in subsequent requests. Also returns cookie named `csrf_access_token` "
                               "that have to be included in X-CSRF-TOKEN header in every request.",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "Successfully logged in"
                        }
                    }
                }
            },
            "400": {
                "$ref": "#components/responses/BadValues"
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
