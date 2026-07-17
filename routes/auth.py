from fastapi import APIRouter, Depends, Response,HTTPException , Request

from sqlalchemy.orm import Session

from core.database import get_db


from schemas.auth import (
    RegisterRequest,
    VerifyOTPRequest,
    ResendOTPRequest,
    LoginRequest,
    ForgotPasswordRequest,
    VerifyForgotOTPRequest,
    ResetPasswordRequest
)

from services.auth_service import (
    register_user,
    verify_registration_otp,
    login_user,
    refresh_access_token,
    logout_user,
    forgot_password,
    verify_forgot_otp,
    reset_password,
    resend_otp
    
)

from fastapi import Cookie
from schemas.auth import LoginRequest
from typing import Annotated
from fastapi import Cookie






router = APIRouter()


@router.post("/register")
def register(
    request: RegisterRequest,
    response: Response,
    db: Session = Depends(get_db)
):

    try:

        result = register_user(
            db,
            request
        )


        response.set_cookie(
            key="otp_token",
            value=result["otp_token"],
            httponly=True,
            max_age=300,
            samesite="lax"
        )

        return {
            "message":
            "OTP sent successfully"
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.post("/verify-otp")
def verify_otp(
    request: VerifyOTPRequest,
    response: Response,
    otp_token: str = Cookie(),
    db: Session = Depends(get_db)
):

    try:

        verify_registration_otp(
            db=db,
            otp=request.otp,
            otp_token=otp_token
        )

        

        return {
            "message":
            "Account activated successfully"
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/login")
def login(
    request: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):

    try:

        result = login_user(
            db,
            request
        )

        response.set_cookie(
            key="access_token",
            value=result["access_token"],
            httponly=True,
            samesite="lax"
        )

        response.set_cookie(
            key="refresh_token",
            value=result["refresh_token"],
            httponly=True,
            samesite="lax"
        )

        return {
            "message": "Login successful"
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )



@router.post("/refresh-token")
def refresh_token_api(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Refresh token missing"
        )

    access_token = refresh_access_token(
        db,
        refresh_token
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax"
    )

    return {
        "message": "Token refreshed"
    }



from fastapi import Request

@router.post("/logout")
def logout(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):

    refresh_token = request.cookies.get("refresh_token")

    logout_user(
        db,
        refresh_token
    )

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    response.delete_cookie("otp_token")
    response.delete_cookie("csrf_token")

    return {
        "message": "Logout successful"
    }

@router.post("/forgot-password")
def forgot_password_api(
    request: ForgotPasswordRequest,
    response: Response,
    db: Session = Depends(get_db)
):

    otp_token = forgot_password(
        db,
        request
    )

    response.set_cookie(
        key="otp_token",
        value=otp_token,
        httponly=True
    )

    return {
        "message": "OTP sent"
    }

@router.post("/verify-forgot-otp")
def verify_forgot_password_otp(
    request: VerifyForgotOTPRequest,
    otp_token: Annotated[str, Cookie()],
    db: Session = Depends(get_db)
):

    verify_forgot_otp(
        db,
        request.otp,
        otp_token
    )

    return {
        "message": "OTP verified"
    }


@router.post("/reset-password")
def reset_password_api(
    request: ResetPasswordRequest,
    response: Response,
    otp_token: Annotated[str, Cookie()],
    db: Session = Depends(get_db)
):

    reset_password(
        db,
        otp_token,
        request
    )

    response.delete_cookie("otp_token")

    return {
        "message": "Password reset successful"
    }

from typing import Annotated
from fastapi import Cookie

from fastapi import Request

@router.post("/resend-otp")
def resend_otp_api(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):

    print(request.cookies)
    otp_token = request.cookies.get("otp_token")

    if not otp_token:
        raise HTTPException(
            status_code=400,
            detail="OTP token not found"
        )

    new_otp_token = resend_otp(db, otp_token)

    response.set_cookie(
        key="otp_token",
        value=new_otp_token,
        httponly=True,
        max_age=300,
        samesite="lax"
    )

    return {"message": "OTP sent successfully"}