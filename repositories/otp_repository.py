from sqlalchemy.orm import Session

from models.otp_verification import OTPVerification


def create_otp(
    db: Session,
    otp_data: dict
):

    otp = OTPVerification(**otp_data)

    db.add(otp)

    db.commit()

    db.refresh(otp)

    return otp


def get_latest_otp(
    db,
    email,
    purpose
):

    return (
        db.query(OTPVerification)
        .filter(
            OTPVerification.email == email,
            OTPVerification.purpose == purpose,
            OTPVerification.verified == False
        )
        .order_by(
            OTPVerification.id.desc()
        )
        .first()
    )


def mark_otp_verified(
    db,
    otp_record
):

    otp_record.verified = True

    db.commit()

    db.refresh(otp_record)

    return otp_record

def delete_existing_otps(
    db,
    email,
    purpose
):

    records = (
        db.query(OTPVerification)
        .filter(
            OTPVerification.email == email,
            OTPVerification.purpose == purpose
        )
        .all()
    )

    for record in records:
        db.delete(record)

    db.commit()