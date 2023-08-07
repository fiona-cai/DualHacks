from firebase_admin import firestore
from google.cloud.firestore_v1 import FieldFilter

from models.question import Question
from database.firestore_setup import cred, firestore_app


def get_question_by_id(question_id):
    """
    returns None if question not found
    :param question_id:
    :return:
    """
    global db

    result = db.collection("questions").document(str(question_id))
    loaded_user = result.get()
    if not loaded_user.exists:
        return None

    return Question(**(loaded_user.to_dict()))


def get_questions_by_subject_and_difficulty(subject, difficulty):
    """
    returns empty array if no question with specified subject found
    :param difficulty:
    :param subject:
    :return:
    """
    global db

    results = list(db.collection("questions").where(filter=FieldFilter("subject", "==", subject)).where(
        filter=FieldFilter("difficulty", "==", difficulty)).stream())

    questions = [Question(**result.to_dict()) for result in results]
    return questions


def add_question(question):
    """
    False for failure
    True for successful operation
    :param question:
    :return:
    """
    global db

    doc_ref = db.collection("questions").document(question.question_id)
    doc_ref.set(question.__dict__)


def delete_question(question):
    """
    False for failure
    True for successful operation
    :param question:
    :return:
    """
    global db

    doc_ref = db.collection("questions").document(question.question_id)
    doc_ref.delete()


def delete_question_by_id(question_id):
    """
    False for failure
    True for successful operation
    :param question_id:
    :return:
    """
    global db

    doc_ref = db.collection("questions").document(question_id)
    doc_ref.delete()


db = firestore.client()

if __name__ == '__main__':
    # question="", answer="", options=[], difficulty=None, subject="", question_id=""
    question_prompt = ""
    answer = ""
    options = [
        "",
        "",
        "",
        ""
    ]
    difficulty = 0  # should be 1, 2, or 3
    subject = ""
    question_id = 1 # add one to this everytime you run

    question = Question(question_prompt, answer, options, difficulty, subject, question_id)
    add_question(question)
    # I think that should be it

