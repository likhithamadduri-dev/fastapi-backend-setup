from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from core.database import get_db

from core.dependencies import (
    get_current_user
)
from schemas.user import (
    UpdateProfileRequest,
    ChangePasswordRequest
)

from services.user_service import (
    get_profile,
    update_profile,
    change_password
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



@router.get("/profile")
def profile(

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_user
    )
):

    try:

        return get_profile(
            db,
            current_user
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

@router.put("/profile")
def update_user_profile_api(

    request: UpdateProfileRequest,

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_user
    )
):

    try:

        update_profile(
            db,
            current_user,
            request
        )

        return {
            "message":
            "Profile updated successfully"
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.post("/change-password")
def change_user_password(

    request: ChangePasswordRequest,

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_user
    )
):

    try:

        change_password(
            db,
            current_user,
            request
        )

        return {

            "message":
            "Password changed successfully"

        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

