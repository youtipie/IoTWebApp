spec = {
    "UnauthorizedError": {
        "description": "No token provided",
        "content": {
            "application/json": {
                "example": {
                    "msg": "Missing Authorization Header."
                }
            }
        }
    },
    "User404": {
        "description": "User does not exist",
        "content": {
            "application/json": {
                "example": {
                    "message": "User with such id does not exist."
                }
            }
        }
    },
    "BadValues": {
        "description": "Missing required fields in request body",
        "content": {
            "application/json": {
                "example": {
                    "message": "Request body must be JSON and contain username, email and password"
                }
            }
        }
    },
    "NotAdmin": {
        "description": "This operation can only be executed if you are admin of network",
        "content": {
            "application/json": {
                "example": {
                    "message": "You are not admin of this network"
                }
            }
        }
    },
    "500": {
        "description": "Internal error",
        "content": {
            "application/json": {
                "example": {
                    "message": "Something went wrong. Try again later"
                }
            }
        }
    }
}
