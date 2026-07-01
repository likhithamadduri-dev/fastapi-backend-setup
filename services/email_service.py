import smtplib

from email.mime.text import MIMEText

from core.config import settings


def send_otp_email(
    email: str,
    otp: str
):

    subject = "OTP Verification"

    body = f"""
Hello,

Your OTP is: {otp}

This OTP will expire in 5 minutes.

Thank You
"""

    message = MIMEText(body)

    message["Subject"] = subject
    message["From"] = settings.EMAIL_USERNAME
    message["To"] = email

    try:

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            settings.EMAIL_USERNAME,
            settings.EMAIL_PASSWORD
        )

        server.sendmail(
            settings.EMAIL_USERNAME,
            email,
            message.as_string()
        )

        server.quit()

        print(
            f"OTP sent successfully to {email}"
        )

        return True

    except Exception as e:

        print(
            f"Email sending failed: {str(e)}"
        )

        return False