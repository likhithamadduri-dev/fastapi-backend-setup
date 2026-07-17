from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional


class CreateTenantUserRequest(BaseModel):

    full_name: str

    email: EmailStr

    password: str

    role: str


class UpdateTenantUserRequest(BaseModel):

    full_name: Optional[str] = None

    role: Optional[str] = None


class UpdateUserStatusRequest(BaseModel):

    is_active: bool


class TenantUserResponse(BaseModel):

    id: int

    full_name: str

    email: EmailStr

    role: str

    is_active: bool

    class Config:

        from_attributes = True