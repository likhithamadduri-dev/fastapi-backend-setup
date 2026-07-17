from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from core.database import get_db

from core.dependencies import (
    get_current_user,
    get_current_organization_user

)

from schemas.organization import (
    UpdateOrganizationProfileRequest
)

from services.organization_service import (
    get_organization_profile,
    update_organization_profile
)

router = APIRouter(

    prefix="/organizations",

    tags=["Organization"]

)

@router.get("/profile")
def organization_profile(

    db: Session = Depends(get_db),

   current_user = Depends(
    get_current_organization_user
)
):

    try:

        return get_organization_profile(

            db,

            current_user

        )

    except ValueError as e:

        raise HTTPException(

            status_code=404,

            detail=str(e)

        )

@router.put("/Updateprofile")
def update_profile(

    request: UpdateOrganizationProfileRequest,

    db: Session = Depends(get_db),

    current_user = Depends(
    get_current_organization_user
)
):

    try:

        update_organization_profile(

            db,

            current_user,

            request

        )

        return {

            "message":

            "Organization profile updated successfully"

        }

    except ValueError as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )