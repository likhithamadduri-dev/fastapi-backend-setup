from sqlalchemy.orm import Session
from models.user import User


def create_tenant_user(
    db: Session,
    user_data: dict
):

    user = User(**user_data)

    db.add(user)

    db.commit()

    db.refresh(user)

    return user

def get_tenant_users(
    db: Session,
    tenant_id: int
):

    return (
        db.query(User)
        .filter(User.tenant_id == tenant_id)
        .all()
    )

def get_tenant_user_by_id(
    db: Session,
    tenant_id: int,
    user_id: int
):

    return (
        db.query(User)
        .filter(
            User.id == user_id,
            User.tenant_id == tenant_id
        )
        .first()
    )

def update_tenant_user(
    db: Session,
    user,
    data: dict
):

    for key, value in data.items():

        setattr(
            user,
            key,
            value
        )

    db.commit()

    db.refresh(user)

    return user

def update_user_status(
    db: Session,
    user,
    is_active: bool
):

    user.is_active = is_active

    db.commit()

    db.refresh(user)

    return user


def delete_tenant_user(
    db: Session,
    user
):

    db.delete(user)

    db.commit()


def get_total_users(
    db,
    tenant_id
):

    return (

        db.query(User)

        .filter(
            User.tenant_id == tenant_id
        )

        .count()

    )


def get_active_users(
    db,
    tenant_id
):

    return (

        db.query(User)

        .filter(
            User.tenant_id == tenant_id,
            User.is_active == True
        )

        .count()

    )


def get_inactive_users(
    db,
    tenant_id
):

    return (

        db.query(User)

        .filter(
            User.tenant_id == tenant_id,
            User.is_active == False
        )

        .count()

    )