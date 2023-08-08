import os
import secrets
import sys
from helpers import get_email_pass, get_hcaptcha_secret

# DO NOT MODIFY THESE SETTINGS! Scroll down to line 24 for settings that you should change
# The secret key is located in secret_key.txt by default
try:
    with open("private_data/secret-key.txt", "r") as file:
        secret_key = file.readline().strip()
        SECRET_KEY = secret_key
except Exception as e:
    sys.stderr.write(str(e))
    secret = secrets.token_hex(48)  # 384 bits
    with open("private_data/secret-key.txt", "w+") as file:
        file.write(secret)
        secret_key = file.readline().strip()
        SECRET_KEY = secret_key

TEMPLATES_AUTO_RELOAD = True
SESSION_PERMANENT = True
SESSION_COOKIE_PATH = "/"
SESSION_TYPE = "filesystem"
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_HTTPONLY = True
SESSION_FILE_DIR = "session"
os.makedirs(SESSION_FILE_DIR, 0o770, True)

# Configure your email settings here
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = "dualhacks2023@gmail.com"
MAIL_PASSWORD = get_email_pass()
MAIL_DEFAULT_SENDER = ("Dual Hacks Participants", "dualhacks2023@gmail.com")

# Configure your hcaptcha settings here
USE_CAPTCHA = False
HCAPTCHA_SECRET = get_hcaptcha_secret()
HCAPTCHA_SITE = "site_key"

"""
LOGGING_FILE_LOCATION should store a path (relative or absolute) to the location of your
site logs. It is recommended to leave it alone, however, if you change it, you should also
change it in daily_tasks.py.
"""
LOGGING_FILE_LOCATION = "logs/server.log"

"""
SESSION_COOKIE_SECURE controls whether the session cookie (and other cookies) should only
be served over HTTPS. Change it to False if your club does not support HTTPS or unexpected
errors are happening.
"""
SESSION_COOKIE_SECURE = True
