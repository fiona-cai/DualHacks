from models.base_model import BaseModel


class Player(BaseModel):
    def __init__(self, user_id="", character=None, points=0):
        self.user_id = user_id
        self.character = character
        self.points = points