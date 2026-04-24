from fastapi import HTTPException

class APIException(HTTPException):

    def __init__(self, status_code: int, error_code: str, message: str):
        self.error_code = error_code

        super().__init__(
            status_code=status_code,
            detail={
                "success": False,
                "error_code": error_code,
                "message": message
            }
        )