from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from core.database import get_db

from core.dependencies import (
    get_current_tenant_admin
)

from schemas.tenant import (
    CreateTenantUserRequest,
    UpdateTenantUserRequest,
    UpdateUserStatusRequest
)

from services.tenant_service import (
    create_organization_user,
    list_organization_users,
    get_organization_user,
    update_organization_user,
    change_user_status,
    remove_organization_user
)


router = APIRouter(
    prefix="/tenant",
    tags=["Tenant"]
)

@router.post("/create-user")
def create_user(

    request: CreateTenantUserRequest,

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_tenant_admin
    )
):

    try:

        create_organization_user(
            db,
            current_user,
            request
        )

        return {

            "message":
            "Organization user created successfully"

        }

    except ValueError as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )

@router.get("/users")
def get_users(

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_tenant_admin
    )
):

    return list_organization_users(
        db,
        current_user
    )

@router.get("/users/{user_id}")
def get_user(

    user_id: int,

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_tenant_admin
    )
):

    try:

        return get_organization_user(
            db,
            current_user,
            user_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

@router.put("/users/{user_id}")
def update_user(

    user_id: int,

    request: UpdateTenantUserRequest,

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_tenant_admin
    )
):

    try:

        update_organization_user(
            db,
            current_user,
            user_id,
            request
        )

        return {

            "message":
            "User updated successfully"

        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

@router.patch("/users/{user_id}/status")
def update_status(

    user_id: int,

    request: UpdateUserStatusRequest,

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_tenant_admin
    )
):

    try:

        change_user_status(
            db,
            current_user,
            user_id,
            request
        )

        return {

            "message":
            "User status updated successfully"

        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.delete("/users/{user_id}")
def delete_user(

    user_id: int,

    db: Session = Depends(get_db),

    current_user = Depends(
        get_current_tenant_admin
    )
):

    try:

        remove_organization_user(
            db,
            current_user,
            user_id
        )

        return {

            "message":
            "User deleted successfully"

        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )