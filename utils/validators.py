def not_empty(value):
    return bool(value.strip())


def valid_email(email):
    email = email.strip()
    return "@" in email and "." in email.split("@")[-1]
