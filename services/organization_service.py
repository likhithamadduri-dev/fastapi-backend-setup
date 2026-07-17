from repositories.tenant_repository import (

    get_tenant_by_id,

    update_tenant

)

from repositories.tenant_user_repository import (

    get_total_users,

    get_active_users,

    get_inactive_users

)

def get_organization_profile(
    db,
    current_user
):

    tenant = get_tenant_by_id(

        db,

        current_user.tenant_id

    )

    if not tenant:

        raise ValueError(

            "Organization not found"

        )

    return tenant

def update_organization_profile(
    db,
    current_user,
    request
):

    tenant = get_tenant_by_id(

        db,

        current_user.tenant_id

    )

    if not tenant:

        raise ValueError(

            "Organization not found"

        )

    data = request.model_dump(

        exclude_unset=True

    )

    return update_tenant(

        db,

        tenant,

        data

    )

def organization_dashboard(
    db,
    current_user
):

    return {

        "organization_name":
        current_user.organization_name,

        "total_users":
        get_total_users(
            db,
            current_user.tenant_id
        ),

        "active_users":
        get_active_users(
            db,
            current_user.tenant_id
        ),

        "inactive_users":
        get_inactive_users(
            db,
            current_user.tenant_id
        )

    }