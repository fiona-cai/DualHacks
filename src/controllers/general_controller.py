from flask import Blueprint, render_template, request, redirect, url_for

general_blueprint = Blueprint("general", __name__)


@general_blueprint.route("/")
@general_blueprint.route("/home/")
def home():
    return render_template("home.html")


@general_blueprint.route("/login/", methods=["POST","GET"])
def login():
    if request.methods == "POST":
        user = request.form[""]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("login.html")


@general_blueprint.route("/user/<username>/profile", methods=["GET"])
def profile():
    return render_template("profile.html")


@general_blueprint.route("/signup/", methods=["POST"])
def signup():
    return render_template("signup.html")


@general_blueprint.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

