from flask import Blueprint, render_template, request, redirect, url_for, session
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

    # get the user with username, if does not exist return back to login.html with an error message
    # check password, if wrong return back to login.html with an error message
    user = users_db.get_user_by_username(request.form["username"])  # get_user_by_username will not check anything it will return a user object
    # you are garanteed that the returned user will have that username so you don't need to check it (its called get by username)

    if user is None: # == None would do the same thing
        pass # change this rendering login but with the "username does not exist message"

    if user.password != request.form["password"]:
        # add the "password is not correct message
        return redirect("login.html")  # don't do redirect here it is the url we are on
        # add error message with flask flashes

    # we get to this point of code if the username exists and if the password is correct
    
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
