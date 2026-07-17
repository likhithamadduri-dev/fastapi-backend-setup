from datetime import datetime ,timedelta

from repositories.user_repository import (
    get_user_by_email,
    create_user,
    activate_user
)


from repositories.tenant_repository import (
    create_tenant
)

from services.otp_service import (
    generate_otp
)

from services.email_service import (
    send_otp_email
)

from core.security import (
    hash_password,
    create_otp_token,
    decode_token,
    verify_password,
    create_refresh_token,
    create_access_token,
    
)


from services.email_validation_service import (
    is_personal_email,
    is_business_email
)

from repositories.user_repository import (
    update_password
)

import re


def register_user(
    db,
    request
):

    existing_user = get_user_by_email(
        db,
        request.email
    )

    if existing_user:

        raise ValueError(
            "Email already registered"
        )

    if request.password != request.confirm_password:

        raise ValueError(
            "Passwords do not match"
        )

    if (
        request.account_type.lower()
        == "organization"
        and not request.organization_name
    ):

        raise ValueError(
            "Organization name required"
        )

    if request.account_type.lower() == "individual":

        if not is_personal_email(
            request.email
        ):

            raise ValueError(
                "Individual account requires personal email"
            )

    if request.account_type.lower() == "organization":

        if not is_business_email(
            request.email
        ):

            raise ValueError(
                "Organization account requires business email"
            )

    if len(request.password) < 8:

        raise ValueError(
            "Password must be at least 8 characters"
        )

    if not re.search(r"[A-Z]", request.password):

        raise ValueError(
            "Password must contain uppercase letter"
        )

    if not re.search(r"[a-z]", request.password):

        raise ValueError(
            "Password must contain lowercase letter"
        )

    if not re.search(r"\d", request.password):

        raise ValueError(
            "Password must contain number"
        )

    if not re.search(
        r"[!@#$%^&*(),.?\":{}|<>]",
        request.password
    ):

        raise ValueError(
            "Password must contain special character"
        )

    hashed_password = hash_password(
        request.password
    )

    role = "individual"

    if request.account_type.lower() == "organization":

        role = "tenant_admin"

    otp = generate_otp()

    send_otp_email(
        request.email,
        otp
    )

    otp_token = create_otp_token(
        {
            "full_name": request.full_name,
            "email": request.email,
            "password_hash": hashed_password,
            "account_type": request.account_type,
            "organization_name": request.organization_name,
            "role": role,
            "otp": otp
        }
    )

    return {

        "otp_token": otp_token

    }


def verify_registration_otp(
    db,
    otp,
    otp_token
):

    if not otp_token:

        raise ValueError(
            "OTP token not found"
        )

    payload = decode_token(
        otp_token
    )

    print("JWT OTP :", payload["otp"])
    print("USER OTP:", otp)

    if not payload:

        raise ValueError(
            "Invalid OTP token"
        )

    if int(payload["otp"]) != int(otp):
     raise ValueError("Invalid OTP")

    existing_user = get_user_by_email(
        db,
        payload["email"]
    )

    if existing_user:

        raise ValueError(
            "Email already registered"
        )

    user = create_user(
        db,
        {
            "full_name": payload["full_name"],
            "email": payload["email"],
            "password_hash": payload["password_hash"],
            "account_type": payload["account_type"],
            "organization_name": payload["organization_name"],
            "role": payload["role"],
            "is_active": False
        }
    )

    if (
        user.account_type.lower() == "organization"
        and user.organization_name
    ):

        create_tenant(
            db,
            user.organization_name,
            user.id
        )

    activate_user(
        db,
        user.email
    )

    return user



def login_user(
    db,
    request
):

    user = get_user_by_email(
        db,
        request.email
    )

    if not user:

        raise ValueError(
            "User not found or inactive"
        )

    if not verify_password(
        request.password,
        user.password_hash
    ):

        raise ValueError(
            "Invalid credentials"
        )

    access_token = create_access_token(
        {
            "user_id": user.id,
            "email": user.email
        }
    )

    refresh_token = create_refresh_token(
        {
            "user_id": user.id,
            "email": user.email
        }
    )



    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


from core.security import (
    decode_token,
    create_access_token
)


def refresh_access_token(
    db,
    refresh_token
):

    if not refresh_token:

        raise ValueError(
            "Refresh token missing"
        )

    payload = decode_token(
        refresh_token
    )

    if not payload:

        raise ValueError(
            "Invalid refresh token"
        )

    '''token_record = get_refresh_token(
        db,
        refresh_token
    )

    if not token_record:

        raise ValueError(
            "Refresh token not found"
        )'''

    access_token = create_access_token(
        {
            "user_id": payload["user_id"],
            "email": payload["email"]
        }
    )

    return access_token



def logout_user(
    db,
    refresh_token
):

    return True


def forgot_password(
    db,
    request
):

    user = get_user_by_email(
        db,
        request.email
    )

    if not user:

        raise ValueError(
            "User not found"
        )

    otp = generate_otp()

    send_otp_email(
        request.email,
        otp
    )

    otp_token = create_otp_token(
        {
            "email": request.email,
            "otp": otp
        }
    )

    return otp_token

def verify_forgot_otp(
    db,
    otp,
    otp_token
):

    if not otp_token:

        raise ValueError(
            "OTP token missing"
        )

    payload = decode_token(
        otp_token
    )

    if not payload:

        raise ValueError(
            "Invalid OTP token"
        )

    if payload["otp"] != otp:

        raise ValueError(
            "Invalid OTP"
        )

    return True

def reset_password(
    db,
    otp_token,
    request
):

    if not otp_token:

        raise ValueError(
            "OTP token missing"
        )

    payload = decode_token(
        otp_token
    )

    if not payload:

        raise ValueError(
            "Invalid OTP token"
        )

    email = payload["email"]

    if (
        request.new_password
        != request.confirm_password
    ):

        raise ValueError(
            "Passwords do not match"
        )

    hashed_password = hash_password(
        request.new_password
    )

    update_password(
        db,
        email,
        hashed_password
    )

    return True

def resend_otp(
    db,
    otp_token
):

    if not otp_token:

        raise ValueError(
            "OTP token not found"
        )

    payload = decode_token(
        otp_token
    )

    if not payload:

        raise ValueError(
            "Invalid OTP token"
        )

    otp = generate_otp()

    print("NEW OTP:", otp)

    send_otp_email(
        payload["email"],
        otp
    )

    new_otp_token = create_otp_token(
        {
            "full_name": payload.get("full_name"),
            "email": payload["email"],
            "password_hash": payload.get("password_hash"),
            "account_type": payload.get("account_type"),
            "organization_name": payload.get("organization_name"),
            "role": payload.get("role"),
            "otp": otp
        }
    )

    print("NEW TOKEN:", new_otp_token)

    return new_otp_token