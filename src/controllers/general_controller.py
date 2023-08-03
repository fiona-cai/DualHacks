from flask import Blueprint, render_template, request

general_blueprint = Blueprint("general", __name__)


@general_blueprint.route("/")
@general_blueprint.route("/home/")
def home():
    return render_template("home.html")


@general_blueprint.route("/login/", methods=["POST","GET"])
def login():
    if request.methods == "POST":
        user = request.form[""]
    else:
        return render_template("login.html")


@general_blueprint.route("/user/<username>/profile", methods=["GET"])
def user():
    return render_template("profile.html")


@general_blueprint.route("/signup/", methods=["POST"])
def signup():
    return render_template("signup.html")



