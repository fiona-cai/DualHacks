from flask import Blueprint, render_template

general_blueprint = Blueprint("general", __name__)


@general_blueprint.route("/")
@general_blueprint.route("/home/")
def home():
    return render_template("home.html")

@general_blueprint.route("/login/", methods=["POST","GET"])
def login():
    return render_template("login.html")

@general_blueprint.route("/<usr>")
def user(usr):
    return f'<h1>{usr}</h1>'

@general_blueprint.route("/signup/")
def signup():
    return render_template("signup.html")



