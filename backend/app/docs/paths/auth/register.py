spec = {
    "post": {
        "summary": "Register new user",
        "description": "Creating a new User and then assigning a default network to him.",
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
                            "username": {
                                "type": "string"
                            },
                            "email": {
                                "type": "string"
                            },
                            "password": {
                                "type": "string"
                            }
                        },
                        "example": {
                            "username": "user",
                            "email": "user@gmail.com",
                            "password": "verySecured8CharPass"
                        }
                    }
                }
            }
        },
        "responses": {
            "201": {
                "description": "The newly registered user",
                "content": {
                    "application/json": {
                        "$ref": "#components/examples/User"
                    }
                }
            },
            "400": {
                "$ref": "#components/responses/BadValues"
            },
            "409": {
                "description": "Invalid email or password",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "User with such username or email already exists."
                        }
                    }
                }
            }
        }
    }
}
