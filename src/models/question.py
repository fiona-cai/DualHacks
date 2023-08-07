from models.base_model import BaseModel


class Question(BaseModel):
    def __init__(self, question="", answer="", options=[], difficulty=None, subject="", question_id=""):
        self.question = question
        self.answer = answer
        self.options = options
        self.difficulty = difficulty
        self.subject = subject
        self.question_id = question_id
