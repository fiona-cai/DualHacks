from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message

import database.users_db_manager as users_db


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

    user = users_db.get_user_by_username(request.form["username"])  # get_user_by_username will not check anything it will return a user object
    # you are garanteed that the returned user will have that username so you don't need to check it (its called get by username)

    # get the user with username, if does not exist return back to login.html with an error message
    if user is None: # == None would do the same thing
        flash("The username you have entered does not exist, please try again.", "warning")  # change this rendering login but with the "username does not exist message"
        return redirect("/")

    # check password, if wrong return back to login.html with an error message
    if user.password != request.form["password"]:
        # add the "password is not correct message
        flash("You have entered the wrong password, please try again.", "warning")
        return redirect("/")  # don't do redirect here it is the url we are on
        # add error message with flask flashes

    # we get to this point of code if the username exists and if the password is correct
    
    # basically setting cookies
    session["username"] = username

    return redirect("/")


@general_blueprint.route("/users/<username>/profile")
def profile():
    # get the user data with username
    userInfo = users_db.get_user_by_username("username") 
    # pass the user object as part of the render_template
    return render_template("profile.html", userInfo = userInfo)


@general_blueprint.route("/signup/", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    # Reached by POST
    if request.method == "POST":
        return render_template("signup.html")

    # check username doesn't already exist
    usernameSignup = users_db.get_user_by_username(request.form["username"])
    if usernameSignup is None: # == None would do the same thing
        pass
    else:
        flash("The username you have entered already exist, please enter another usename.", "warning") 

    # check if all information are provided

    # send an email
    # get their email



    # redirect to login with a message that a confirmation email has been sent
    flash("A confirmation email has been sent, please check your inbox.", "info")
    return redirect("login.html")

