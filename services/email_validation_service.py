PERSONAL_DOMAINS = [
    "gmail.com",
    "yahoo.com",
    "outlook.com",
    "hotmail.com",
    "icloud.com"
]


def is_personal_email(email: str):

    domain = email.split("@")[-1].lower()

    return domain in PERSONAL_DOMAINS


def is_business_email(email: str):

    domain = email.split("@")[-1].lower()

    return domain not in PERSONAL_DOMAINS