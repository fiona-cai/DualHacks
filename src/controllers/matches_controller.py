from flask import Blueprint, render_template, session, redirect, flash
from models.player import Player
from models.match import Match
import database.match_db_manager as match_db
import database.character_db_manager as character_db
from helpers import login_required

matches_blueprint = Blueprint("matches", __name__)


@matches_blueprint.route("/quick")
@login_required
def quick_match():
    if session.get("character") is None:
        return redirect("/choose-character")
    character = character_db.get_character_by_name(session["character"])
    match = match_db.add_to_available_match(Player(session["username"], character.name, 0, None, character.health))
    if not match:
        return redirect("/matches/create")

    match.player_count += 1
    match_db.update_match(match)
    return redirect(f"/matches/{match.match_id}")


@matches_blueprint.route("/create")
@login_required
def create_match():
    match = Match(int(match_db.get_last_match_id()) + 1)
    match_db.add_match(match)
    return redirect(f"/matches/{match.match_id}/join")


@matches_blueprint.route("/<match_id>/join", methods=["GET"])
@login_required
def join_match(match_id):
    if session.get("character") is None:
        return redirect("/choose-character")

    match = match_db.get_match_by_id(match_id)
    if match is None:
        flash("The game you are trying to load does not exist", "warning")
        return redirect("/")

    character = character_db.get_character_by_name(session["character"])
    match_db.add_player_to_match(match_id, Player(session["username"], character.name, 0, None, character.health))


    match.player_count += 1
    match_db.update_match(match)

    return redirect(f"/matches/{match.match_id}")


@matches_blueprint.route("/<match_id>/submit-answer", methods=["POST"])
@login_required
def submit_answer(match_id):
    pass


@matches_blueprint.route("/<match_id>")
@login_required
def get_match(match_id):
    match = match_db.get_match_by_id(match_id)
    if match is None:
        flash("The game you are trying to load does not exist", "warning")
        return redirect("/")
    return render_template("match/match.html", match_info=match)
