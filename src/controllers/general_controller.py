from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash
import jwt
from datetime import datetime
import sys

import database.users_db_manager as users_db
import database.character_db_manager as character_db
from helpers import create_jwt, send_email, login_required
from models.user import User
from settings import MAIL_DEFAULT_SENDER, SECRET_KEY

general_blueprint = Blueprint("general", __name__)


@general_blueprint.route("/")
@general_blueprint.route("/home")
def home():
    return render_template("home.html")


@general_blueprint.route("/login", methods=["POST", "GET"])
def login():
    session.clear()
    session.permanent = True

    if request.method == "GET":
        return render_template("login.html")

    # Reached by POST
    username = request.form["username"]

    user = users_db.get_user_by_username(request.form["username"])

    if user is None:
        flash("The username you have entered does not exist, please try again.", "warning")
        return render_template("login.html")

    if user.password != request.form["password"]:
        flash("You have entered the wrong password, please try again.", "warning")
        return render_template("login.html")

    session["username"] = username

    return redirect("/")


@general_blueprint.route("/users/<username>/profile")
def profile(username):
    user_info = users_db.get_user_by_username(username)
    return render_template("profile.html", user_info=user_info)


@general_blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    # Reached by POST

    username_signup = users_db.get_user_by_username(request.form["username"])
    if username_signup:
        flash("The username you have entered already exist, please enter another username.", "warning")
        return render_template("signup.html")

    # check if all information are provided
    if request.form["username"] is None:
        flash("You need to add the username", "warning")
        return render_template("signup.html")

    user = User(request.form["username"], request.form["name"], request.form["lastname"],
                request.form["email"], request.form["password"])
    users_db.add_user(user)

    token = create_jwt({'email': user.email, 'username': user.username}, SECRET_KEY)
    text = render_template('confirmation_email.html', username=user.username, token=token)

    send_email('Account Confirmation', MAIL_DEFAULT_SENDER, [user.email], text)

    flash("A confirmation email has been sent, please check your inbox.", "info")
    return redirect("/login")


@general_blueprint.route('/confirmregister/<token>')
def confirm_register(token):
    try:
        token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except Exception as e:
        sys.stderr.write(str(e))
        token = 0
    if not token:
        flash("Email verification link invalid", "warning")
        return redirect("/register")

    user = users_db.get_user_by_username(token['username'])

    if datetime.strptime(token["expiration"], "%Y-%m-%dT%H:%M:%S.%f") < datetime.utcnow():
        users_db.delete_user(user)
        flash("Email verification link expired. Please register again using the same email.", "warning")
        return redirect("/register")

    user.verified = True
    users_db.update_user(user)

    return redirect("/login")


@general_blueprint.route("/choose-character", methods=["GET", "POST"])
@login_required
def choose_character():
    characters = character_db.get_all_characters()
    if request.method == "GET":
        session["character"] = "Evil Math Professor"
        return render_template("choose_character.html", characters=characters)

    session["character"] = request.form["character"]
    return redirect("/matches/quick")
