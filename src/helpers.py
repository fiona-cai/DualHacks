from flask import request, redirect, session
from flask_mail import Message
from functools import wraps
import jwt
from datetime import datetime, timedelta


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


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(session.get("username"))
        if session.get("username") is None:
            return redirect("/login?next=" + request.path)
        return f(*args, **kwargs)
    return decorated_function

def create_jwt(data, secret_key, time=1800):
    """
    Creates a JWT token containing data and encrypted using secret_key
    """
    data['expiration'] = (datetime.utcnow() + timedelta(seconds=time)).isoformat()
    return jwt.encode(data, secret_key, algorithm='HS256')


def send_email(subject, sender, recipients, text, bcc=None):
    from setup import mail
    message = Message(subject, sender=sender, recipients=recipients, html=text, bcc=bcc)
    mail.send(message)
