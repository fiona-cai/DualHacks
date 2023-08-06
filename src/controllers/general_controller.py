from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash

import database.users_db_manager as users_db
from models.user import User

general_blueprint = Blueprint("general", __name__)


@general_blueprint.route("/")
@general_blueprint.route("/home/")
def home():
    return render_template("home.html")


@general_blueprint.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    # Reached by POST
    username = request.form["username"]
    password = request.form["password"]

    user = users_db.get_user_by_username(
        request.form["username"])  # get_user_by_username will not check anything it will return a user object
    # you are garanteed that the returned user will have that username so you don't need to check it (its called get by username)

    # get the user with username, if does not exist return back to login.html with an error message
    if user is None:  # == None would do the same thing
        flash("The username you have entered does not exist, please try again.",
              "warning")  # change this rendering login but with the "username does not exist message"
        return render_template("/")

    # check password, if wrong return back to login.html with an error message
    if user.password != request.form["password"]:
        # add the "password is not correct message
        flash("You have entered the wrong password, please try again.", "warning")
        return render_template("/")  # don't do redirect here it is the url we are on
        # add error message with flask flashes

    # we get to this point of code if the username exists and if the password is correct

    # basically setting cookies
    session["username"] = username

    return render_template("/")


@general_blueprint.route("/users/<username>/profile")
def profile(username):
    # get the user data with username
    user_info = users_db.get_user_by_username(username)
    # pass the user object as part of the render_template
    return render_template("profile.html", user_info=user_info)


@general_blueprint.route("/signup/", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    # Reached by POST
    if request.method == "POST":
        return render_template("signup.html")

    # check username doesn't already exist
    usernameSignup = users_db.get_user_by_username(request.form["username"])
    if usernameSignup:  # this would mean that user is not None
        flash("The username you have entered already exist, please enter another username.", "warning")
        # return the user back to the

    # check if all information are provided
    this_user_info = User(request.form["username"],request.form["name"],request.form["lastname"],request.form["email"],request.form["password"])
    add_this_user_info = users_db.add_user(this_user_info)
    # send an email
    # get their email

    # redirect to login with a message that a confirmation email has been sent
    flash("A confirmation email has been sent, please check your inbox.", "info")
    return render_template("login.html")
