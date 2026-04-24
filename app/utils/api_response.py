from pydantic import BaseModel
from typing import Optional, Any

class CustomAPIResponse(BaseModel):
    success: bool
    data: Optional[Any] = []
    error_code: Optional[str] = ""
    message: Optional[str] = ""