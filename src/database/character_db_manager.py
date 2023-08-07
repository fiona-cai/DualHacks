from firebase_admin import firestore
from google.cloud.firestore_v1 import FieldFilter

from models.character import Character
from database.firestore_setup import cred, firestore_app


def get_character_by_name(name):
    global db

    results = list(db.collection("characters").where(filter=FieldFilter("name", "==", name)).limit(1).stream())
    if len(results) == 0:
        return None

    loaded_character = results[0].to_dict()
    return Character(**loaded_character)


def create_character(character):
    global db

    doc_ref = db.collection("characters").document(character.name)
    doc_ref.set(character.__dict__)


db = firestore.client()
