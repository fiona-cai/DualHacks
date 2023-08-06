from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash

import database.users_db_manager as users_db
from models.user import User

general_blueprint = Blueprint("general", __name__)


@general_blueprint.route("/")
@general_blueprint.route("/home")
def home():
    return render_template("home.html")


@general_blueprint.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    # Reached by POST
    username = request.form["username"]

    user = users_db.get_user_by_username(request.form["username"])

    if user is None:
        flash("The username you have entered does not exist, please try again.", "warning")
        return render_template("/")

    if user.password != request.form["password"]:
        flash("You have entered the wrong password, please try again.", "warning")
        return render_template("/")

    session["username"] = username

    return render_template("/")


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
    # send an email
    # get their email

    flash("A confirmation email has been sent, please check your inbox.", "info")
    return redirect("/login")
