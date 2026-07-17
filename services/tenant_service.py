from repositories.tenant_user_repository import (
    create_tenant_user,
    get_tenant_users,
    get_tenant_user_by_id,
    update_tenant_user,
    update_user_status,
    delete_tenant_user
)

from repositories.user_repository import (
    get_user_by_email
)

from core.security import (
    hash_password
)

def create_organization_user(
    db,
    current_user,
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

    user = create_tenant_user(
        db,
        {
            "full_name": request.full_name,
            "email": request.email,
            "password_hash": hash_password(
                request.password
            ),
            "account_type": "organization",
            "organization_name": current_user.organization_name,
            "role": request.role,
            "tenant_id": current_user.tenant_id,
            "is_active": True
        }
    )

    return user

def list_organization_users(
    db,
    current_user
):

    return get_tenant_users(
        db,
        current_user.tenant_id
    )


def get_organization_user(
    db,
    current_user,
    user_id
):

    user = get_tenant_user_by_id(
        db,
        current_user.tenant_id,
        user_id
    )

    if not user:

        raise ValueError(
            "User not found"
        )

    return user

def update_organization_user(
    db,
    current_user,
    user_id,
    request
):

    user = get_tenant_user_by_id(
        db,
        current_user.tenant_id,
        user_id
    )

    if not user:

        raise ValueError(
            "User not found"
        )

    allowed_roles = [
    "tenant_admin",
    "tenant_user"
]

    if request.role not in allowed_roles:

        raise ValueError(
            "Invalid role"
        )

    if current_user.id == user_id and request.role:

        raise ValueError(
            "Tenant Admin cannot change their own role"
        )

    if request.role and request.role not in allowed_roles:

        raise ValueError(
            "Invalid role"
        )

    data = request.model_dump(
        exclude_unset=True
    )

    return update_tenant_user(
            db,
            user,
            data
        )


def change_user_status(
    db,
    current_user,
    user_id,
    request
):

    user = get_tenant_user_by_id(
        db,
        current_user.tenant_id,
        user_id
    )

    if not user:

        raise ValueError(
            "User not found"
        )

    if current_user.id == user_id and not request.is_active:

        raise ValueError(
            "Tenant Admin cannot deactivate their own account"
        )

    return update_user_status(
        db,
        user,
        request.is_active
    )



def remove_organization_user(
    db,
    current_user,
    user_id
):

    user = get_tenant_user_by_id(
        db,
        current_user.tenant_id,
        user_id
    )

    if not user:

        raise ValueError(
            "User not found"
        )

    if current_user.id == user_id:

        raise ValueError(
            "Tenant Admin cannot delete their own account"
        )

    delete_tenant_user(
        db,
        user
    )

    return True