from datetime import datetime

from models.refresh_token import RefreshToken


def save_refresh_token(
    db,
    user_id,
    token,
    expires_at
):

    refresh_token = RefreshToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at,
        created_at=datetime.utcnow()
    )

    db.add(refresh_token)

    db.commit()

    db.refresh(refresh_token)

    return refresh_token


def get_refresh_token(
    db,
    token
):

    return (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token == token
        )
        .first()
    )


def delete_refresh_token(
    db,
    token
):

    refresh_token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token == token
        )
        .first()
    )

    if refresh_token:
        db.delete(refresh_token)
        db.commit()