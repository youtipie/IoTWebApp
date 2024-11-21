spec = {
    "post": {
        "summary": "Refresh access token",
        "tags": [
            "Auth"
        ],
        "security": [
            {
                "refreshToken": []
            }
        ],
        "responses": {
            "200": {
                "description": "Refreshes user's access token",
                "content": {
                    "application/json": {
                        "example": {
                            "access_token": "asdasflasd.asdasdasdasd.asdasdasd"
                        }
                    }
                }
            },
            "401": {
                "$ref": "#/components/responses/UnauthorizedError"
            }
        }
    }
}
