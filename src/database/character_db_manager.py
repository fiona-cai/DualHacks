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


def get_all_characters():
    global db

    results = list(db.collection("characters").stream())

    characters = [Character(**result.to_dict()) for result in results]
    return characters


def create_character(character):
    global db

    doc_ref = db.collection("characters").document(character.name)
    doc_ref.set(character.__dict__)


db = firestore.client()

if __name__ == '__main__':
    powers = [
        {
            "damage": 1,
            "difficulty": 1,
            "name": "Numerical Eruption"  # change this
        },
        {
            "damage": 2,
            "difficulty": 2,
            "name": "Algebraic Nova"  # change this
        },
        {
            "damage": 3,
            "difficulty": 3,
            "name": "Quantum Amplification"  # change this
        }
    ]

    name = "Evil Math Professor"  # you would need to change this name
    health = 10
    subject = "Math"  # change this
    character = Character(name, powers, f"{name}_image.png", health, subject)
    create_character(character)
    # yea for each character paste the info then run. then change the info and run again. exactly
    # ok so you need to change the names and subject for each of your characters
    # then run this file (not the app this file)
    # oh also you gotta add a file to the private data, I'll give you that in a little bit
