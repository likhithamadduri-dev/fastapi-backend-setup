from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):

    username: str
    email: str
    password: str


class UserResponse(BaseModel):

    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class UpdateProfileRequest(BaseModel):

    full_name: Optional[str] = None

class ChangePasswordRequest(BaseModel):

    current_password: str

    new_password: str

    confirm_password: str