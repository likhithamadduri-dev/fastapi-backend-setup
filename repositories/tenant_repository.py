from models.tenant import Tenant


def create_tenant(
    db,
    organization_name,
    owner_user_id
):

    tenant = Tenant(
        organization_name=organization_name,
        owner_user_id=owner_user_id,
        status="active"
    )

    db.add(tenant)

    db.commit()

    db.refresh(tenant)

    return tenant