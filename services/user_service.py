from repositories.user_repository import (
    get_user_by_id,
    update_user_profile,
    update_password
)
from core.security import (
    verify_password,
    hash_password
)


def get_profile(
    db,
    current_user
):

    user = get_user_by_id(
        db,
        current_user.id
    )

    if not user:

        raise ValueError(
            "User not found"
        )

    return user

def update_profile(
    db,
    current_user,
    request
):

    data = request.model_dump(
        exclude_unset=True
    )

    user = update_user_profile(
        db,
        current_user,
        data
    )

    return user

def change_password(
    db,
    current_user,
    request
):

    if not verify_password(
        request.current_password,
        current_user.password_hash
    ):

        raise ValueError(
            "Current password is incorrect"
        )

    if request.new_password != request.confirm_password:

        raise ValueError(
            "Passwords do not match"
        )

    hashed_password = hash_password(
        request.new_password
    )

    update_password(
        db,
        current_user.email,
        hashed_password
    )

    return True

def individual_dashboard(
    current_user
):

    return {

        "user_id": current_user.id,

        "full_name": current_user.full_name,

        "email": current_user.email,

        "account_type": current_user.account_type,

        "role": current_user.role

    }
