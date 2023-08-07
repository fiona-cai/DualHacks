from flask import Blueprint, render_template, session, redirect, flash
from models.player import Player
from models.match import Match
import database.match_db_manager as match_db
import database.character_db_manager as character_db

matches_blueprint = Blueprint("matches", __name__)


@matches_blueprint.route("/quick")
def quick_match():
    character = character_db.get_character_by_name(session["character"])
    match_id = match_db.add_to_available_match(Player(session["username"], character, 0, None, character.health))
    if not match_id:
        return redirect("matches/create")
    return redirect(f"matches/{match_id}")


@matches_blueprint.route("/create")
def create_match():
    match = Match(match_db.get_last_match_id() + 1)
    match_db.add_match(match)
    return redirect(f"matches/{match.match_id}/join")


@matches_blueprint.route("/<match_id>/join", methods=["POST"])
def join_match(match_id):
    match = match_db.get_match_by_id(match_id)
    if match is None:
        flash("The game you are trying to load does not exist", "warning")
        return redirect("/")
    match.player_count += 1
    match_db.update_match(match)


@matches_blueprint.route("/<match_id>/submit-answer", methods=["POST"])
def submit_answer(match_id):
    pass


@matches_blueprint.route("/<match_id>")
def get_match(match_id):
    match = match_db.get_match_by_id(match_id)
    if match is None:
        flash("The game you are trying to load does not exist", "warning")
        return redirect("/")
    return render_template("match/match.html", match_info=match)
