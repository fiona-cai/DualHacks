def get_email_pass():
    with open("private_data/email-password.txt") as file:
        password = file.readline()
    if not password:
        return None
    return password


def get_hcaptcha_secret():
    with open("private_data/hcaptcha-secret.txt") as file:
        hcaptcha = file.readline()
    if not hcaptcha:
        return None
    return hcaptcha
