class CustomResponse:
    def __init__(self, code:int = 200, msg: str = "", is_success: bool = True, data: None = None):
        self.code = code
        self.message = msg
        self.is_success = is_success
        self.data = data

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
