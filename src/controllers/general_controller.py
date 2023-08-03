from flask import Blueprint, render_template

general_blueprint = Blueprint("general", __name__)


@general_blueprint.route("/")
@general_blueprint.route("/home")
def home():
    return render_template("home.html")
