from models.base_model import BaseModel


class Player(BaseModel):
    def __init__(self, username="", character=None, points=0, client_id="", health=0):
        self.username = username
        self.character = character
        self.points = points
        self.client_id = client_id
        self.health = health
