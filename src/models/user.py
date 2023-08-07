from models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, username="", name="", lastname="", email="", password="", verified=False):
        self.username = username
        self.name = name
        self.lastname = lastname
        self.email = email
        self.password = password
        self.verified = verified
