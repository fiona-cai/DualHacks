from models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, username="", name="", lastname="", age=None, email="", password=""):
        self.username = username
        self.name = name
        self.lastname = lastname
        self.age = age
        self.email = email
        self.password = password
