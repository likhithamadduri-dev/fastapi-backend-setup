from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from core.database import get_db

from core.dependencies import (
    get_current_user
)

from services.user_service import (
    individual_dashboard
)

from services.organization_service import (

    organization_dashboard

)

from core.dependencies import (

    get_current_organization_user

)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/individual")
def get_individual_dashboard(

    current_user = Depends(
        get_current_user
    )
):

    return individual_dashboard(
        current_user
    )

@router.get("/organization")
def get_organization_dashboard(

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_organization_user
    )
):

    return organization_dashboard(
        db,
        current_user
    )