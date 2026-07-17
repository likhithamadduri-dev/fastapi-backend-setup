from fastapi import Cookie
from fastapi import HTTPException
from fastapi import Depends

from sqlalchemy.orm import Session

from core.database import get_db

from core.security import decode_token

from repositories.user_repository import (
    get_user_by_email
)
from core.security import (
    decode_token
)


def get_current_user(
    access_token: str = Cookie(None),
    db: Session = Depends(get_db)
):

    if not access_token:

        raise HTTPException(
            status_code=401,
            detail="Access token missing"
        )

    payload = decode_token(
        access_token
    )

    if not payload:

        raise HTTPException(
            status_code=401,
            detail="Invalid access token"
        )

    user = get_user_by_email(
        db,
        payload["email"]
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


def get_current_tenant_admin(
    current_user = Depends(get_current_user)
):

    if current_user.role != "tenant_admin":

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return current_user

def get_current_organization_user(

    access_token: str = Cookie(None),

    db: Session = Depends(get_db)

):

    if not access_token:

        raise HTTPException(

            status_code=401,

            detail="Access token missing"

        )

    payload = decode_token(
        access_token
    )

    if not payload:

        raise HTTPException(

            status_code=401,

            detail="Invalid access token"

        )

    user = get_user_by_email(

        db,

        payload["email"]

    )

    if not user:

        raise HTTPException(

            status_code=404,

            detail="User not found"

        )

    if user.account_type.lower() != "organization":

        raise HTTPException(

            status_code=403,

            detail="Only organization users can access this resource"

        )

    return user