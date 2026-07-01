from sqlalchemy.orm import Session

from models.user import User


def get_user_by_email(
    db: Session,
    email: str
):

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def create_user(
    db: Session,
    user_data: dict
):

    user = User(**user_data)

    db.add(user)

    db.commit()

    db.refresh(user)

    return user


def activate_user(
    db: Session,
    email: str
):

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        return None

    user.is_active = True

    db.commit()

    db.refresh(user)

    return user

def get_active_user_by_email(
    db,
    email
):

    return (
        db.query(User)
        .filter(
            User.email == email,
            User.is_active == True
        )
        .first()
    )

def update_password(
    db,
    email,
    hashed_password
):

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        return None

    user.password_hash = hashed_password

    db.commit()

    db.refresh(user)

    return user