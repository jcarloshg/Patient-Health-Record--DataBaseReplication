class CustomResponse:
    def __init__(self, code: int = 200, msg: str = "", is_success: bool = True, data: None = None):
        self.code = code
        self.message = msg
        self.is_success = is_success
        self.data = data

    def to_primitives(self) -> dict:
        """Convert the response to primitive dictionary format."""
        return {
            "code": self.code,
            "message": self.message,
            "is_success": self.is_success,
            "data": self.data
        }

    def to_JSON_response(self):
        """Convert the response to JSON response format."""
        return {
            "status_code": self.code,
            "content": {
                "message": self.message,
                "is_success": self.is_success,
                "data": self.data
            }
        }

    @staticmethod
    def success(msg: str = "Success", success: bool = True, data: None = None):
        return CustomResponse(
            msg=msg,
            is_success=success,
            data=data
        )

    @staticmethod
    def error(msg: str = "Error", data: None = None):
        return CustomResponse(
            code=400,
            msg=msg,
            is_success=False,
            data=data
        )
