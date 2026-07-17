from models.tenant import Tenant
from models.user import User


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

    user = (
        db.query(User)
        .filter(User.id == owner_user_id)
        .first()
    )

    user.tenant_id = tenant.id

    db.commit()

    db.refresh(user)

    return tenant

def get_tenant_by_id(
    db,
    tenant_id
):

    return (

        db.query(Tenant)

        .filter(
            Tenant.id == tenant_id
        )

        .first()

    )

def update_tenant(
    db,
    tenant,
    data
):

    for key, value in data.items():

        setattr(
            tenant,
            key,
            value
        )

    db.commit()

    db.refresh(tenant)

    return tenant

