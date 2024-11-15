spec = {
    "post": {
        "summary": "Logout user",
        "tags": [
            "Auth"
        ],
        "responses": {
            "200": {
                "description": "Deletes access token from cookies",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "Successfully logged out"
                        }
                    }
                }
            },
        }
    }
}
