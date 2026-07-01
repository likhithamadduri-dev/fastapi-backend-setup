from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional


class RegisterRequest(BaseModel):

    full_name: str

    email: EmailStr

    password: str

    confirm_password: str

    account_type: str

    organization_name: Optional[str] = None


class VerifyOTPRequest(BaseModel):

    otp: str


class ResendOTPRequest(BaseModel):

    pass


class LoginRequest(BaseModel):

    email: EmailStr

    password: str


class ForgotPasswordRequest(BaseModel):

    email: EmailStr


class VerifyForgotOTPRequest(BaseModel):

    otp: str


class ResetPasswordRequest(BaseModel):

    new_password: str

    confirm_password: str