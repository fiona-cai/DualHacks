from firebase_admin import firestore
from google.cloud.firestore_v1 import FieldFilter

from models.user import User
from database.firestore_setup import cred, firestore_app


def get_user_by_username(username):
    """
    returns None if user not found
    :param username:
    :return: User object
    """
    global db

    result = db.collection("users").document(username)
    loaded_user = result.get()

    if not loaded_user.exists:
        return None

    return User(**(loaded_user.to_dict()))


def get_users_with_name(name):
    """
    returns empty array if user with name not found
    :param name:
    :return: array of User objects
    """
    pass


def add_user(user):
    """
    returns False if operation unsuccessful
    returns True if operation is successful
    :param user:
    :return: boolean
    """
    global db

    doc_ref = db.collection("users").document(user.username)
    doc_ref.set(user.__dict__)


def delete_user(user):
    """
    returns False if operation unsuccessful
    returns True if operation is successful
    :param user:
    :return: boolean
    """
    global db

    doc_ref = db.collection("users").document(user.username)
    doc_ref.delete()


def update_user(user):
    """
    returns False if operation unsuccessful
    returns True if operation is successful
    :param user:
    :return: boolean
    """
    global db

    doc_ref = db.collection("users").document(user.username)
    doc_ref.set(user.__dict__)


def count_users():
    global db

    return db.collection("users").count().get()[0][0].value


db = firestore.client()
