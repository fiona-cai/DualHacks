from models.base_model import BaseModel


class Player(BaseModel):
    def __init__(self, username="", character=None, points=0):
        self.username = username
        self.character = character
        self.points = points
