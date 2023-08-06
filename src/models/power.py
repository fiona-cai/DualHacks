from models.base_model import BaseModel


class Power(BaseModel):
    def __init__(self, subject="", damage=0, difficulty=0):
        self.subject = subject
        self.damage = damage
        self.difficulty = difficulty
