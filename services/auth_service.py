from datetime import datetime
from datetime import timedelta

from repositories.user_repository import (
    get_user_by_email,
    create_user,
    activate_user
)

from repositories.otp_repository import (
    create_otp,
    get_latest_otp,
    mark_otp_verified
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
    decode_token
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

    # NEW VALIDATION

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

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", request.password):
        raise ValueError(
            "Password must contain special character"
        )

    hashed_password = hash_password(
        request.password
    )

    role = "individual"

    if request.account_type.lower() == "organization":
        role = "tenant_admin"
   
    user = create_user(
        db,
        {
            "full_name": request.full_name,
            "email": request.email,
            "password_hash": hashed_password,
            "account_type": request.account_type,
            "organization_name": request.organization_name,
            "role": role,
            "is_active": False
        }
    )

    otp = generate_otp()

    create_otp(
        db,
        {
            "email": request.email,
            "otp": otp,
            "purpose": "registration",
            "verified": False,
            "expires_at": (
                datetime.utcnow()
                + timedelta(minutes=5)
            )
        }
    )

    send_otp_email(
        request.email,
        otp
    )

    otp_token = create_otp_token(
        {
            "email": request.email
        }
    )

    return {
        "user": user,
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

    if not payload:
        raise ValueError(
            "Invalid OTP token"
        )

    email = payload.get(
        "email"
    )

    otp_record = get_latest_otp(
        db,
        email,
        "registration"
    )

    if not otp_record:
        raise ValueError(
            "OTP not found"
        )

    if otp_record.expires_at < datetime.utcnow():
        raise ValueError(
            "OTP expired"
        )

    print("DB OTP =", otp_record.otp)
    print("REQUEST OTP =", otp)
    print("DB OTP TYPE =", type(otp_record.otp))
    print("REQUEST OTP TYPE =", type(otp))


    if otp_record.otp != otp:
        raise ValueError(
            "Invalid OTP"
        )

    mark_otp_verified(
        db,
        otp_record
    )

    user = activate_user(
        db,
        email
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

    return user

from repositories.user_repository import (
    get_active_user_by_email
)

from repositories.refresh_token_repository import (
    save_refresh_token
)

from core.security import (
    verify_password,
    create_access_token,
    create_refresh_token
)

from datetime import datetime
from datetime import timedelta


def login_user(
    db,
    request
):

    user = get_active_user_by_email(
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

    save_refresh_token(
    db=db,
    user_id=user.id,
    token=refresh_token,
    expires_at=(
        datetime.utcnow()
        + timedelta(days=7)
    )
)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

from repositories.refresh_token_repository import (
    get_refresh_token
)

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

    token_record = get_refresh_token(
        db,
        refresh_token
    )

    if not token_record:

        raise ValueError(
            "Refresh token not found"
        )

    access_token = create_access_token(
        {
            "user_id": payload["user_id"],
            "email": payload["email"]
        }
    )

    return access_token

from repositories.refresh_token_repository import (
    delete_refresh_token
)


def logout_user(
    db,
    refresh_token
):

    if refresh_token:

        delete_refresh_token(
            db,
            refresh_token
        )

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

    create_otp(
        db,
        {
            "email": request.email,
            "otp": otp,
            "purpose": "forgot_password",
            "verified": False,
            "expires_at": (
                datetime.utcnow()
                + timedelta(minutes=5)
            )
        }
    )

    otp_token = create_otp_token(
        {
            "email": request.email
        }
    )

    send_otp_email(
    request.email,
    otp
)

    return otp_token

def verify_forgot_otp(
    db,
    otp,
    otp_token
):

    payload = decode_token(
        otp_token
    )

    email = payload["email"]

    otp_record = get_latest_otp(
        db,
        email,
        "forgot_password"
    )

    if not otp_record:

        raise ValueError(
            "OTP not found"
        )

    if otp_record.otp != otp:

        raise ValueError(
            "Invalid OTP"
        )

    mark_otp_verified(
        db,
        otp_record
    )

    if otp_record.expires_at < datetime.utcnow():

        raise ValueError(
            "OTP expired"
        )

    if otp_record.expires_at < datetime.utcnow():

        raise ValueError(
            "OTP expired"
        )

    return True

from repositories.user_repository import (
    update_password
)


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

    email = payload["email"]

    otp = generate_otp()

    create_otp(
        db,
        {
            "email": email,
            "otp": otp,
            "purpose": "registration",
            "verified": False,
            "expires_at": (
                datetime.utcnow()
                + timedelta(minutes=5)
            )
        }
    )

    send_otp_email(
        email,
        otp
    )

    return True