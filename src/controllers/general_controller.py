from flask import Blueprint, render_template, request, redirect, url_for, session

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

    # get the user with username, if does not exist return back to login.html with an error message
    # check password, if wrong password return back to the login.html with an error message

    # basically setting cookies
    session["username"] = username

    return redirect("/")


@general_blueprint.route("/users/<username>/profile")
def profile():
    # get the user data with username
    # pass the user object as part of the render_template

    return render_template("profile.html")


@general_blueprint.route("/signup/", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    # Reached by POST

    # check username doesn't already exist

    # check if all information are provided

    # send an email

    # redirect to login with a message that a confirmation email has been sent
