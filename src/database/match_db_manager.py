from firebase_admin import firestore
from google.cloud.firestore_v1 import FieldFilter

from models.match import Match
from models.player import Player
from database.firestore_setup import cred, firestore_app


def get_match_by_id(match_id):
    global db

    results = list(db.collection("matches").where(filter=FieldFilter("match_id", "==", int(match_id))).limit(1).stream())
    if len(results) == 0:
        return None

    loaded_match = results[0].to_dict()
    return Match(**loaded_match)


def add_match(match):
    global db

    doc_ref = db.collection("matches").document(str(match.match_id))
    doc_ref.set(match.__dict__)


def update_match(match):
    global db

    doc_ref = db.collection("matches").document(str(match.match_id))
    doc_ref.set(match.__dict__)


def delete_match(match_id):
    global db

    doc_ref = db.collection("matches").document(str(match_id))
    doc_ref.delete()


def count_match():
    global db

    return db.collection("matches").count().get()[0][0].value


def get_last_match_id():
    global db

    results = list(db.collection("matches").order_by("match_id", direction=firestore.Query.DESCENDING).limit(1).stream())
    if len(results) == 0:
        return 0

    loaded_match = results[0].to_dict()
    print(loaded_match["match_id"])
    return Match(**loaded_match).match_id


def get_match_players(match_id):
    global db

    results = list(db.collection("matches").document(str(match_id)).collection("players").stream())

    players = [Player(**result.to_dict()) for result in results]
    return players


def add_player_to_match(match_id, player):
    global db

    doc_ref = db.collection("matches").document(str(match_id)).collection("players").document(player.username)
    doc_ref.set(player.__dict__)


def add_to_available_match(player):
    """
    return None if there is no available game to join
    :param player:
    :return:
    """
    global db

    results = list(db.collection("matches").order_by("player_count").limit(1).stream())
    if len(results) == 0:
        return None

    loaded_match = results[0].to_dict()
    match = Match(**loaded_match)
    print(match.__dict__)
    if match.player_count >= 2:
        return None

    add_player_to_match(match.match_id, player)
    return match


def update_player(match_id, player):
    global db

    doc_ref = db.collection("matches").document(str(match_id)).collection("players").document(player.username)
    doc_ref.set(player.__dict__)


db = firestore.client()
