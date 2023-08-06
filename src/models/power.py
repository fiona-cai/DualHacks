from models.base_model import BaseModel


class Power(BaseModel):
    def __init__(self, damage=0, difficulty=0, name=""):
        self.damage = damage
        self.difficulty = difficulty
        self.name = name
