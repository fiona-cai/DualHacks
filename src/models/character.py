from models.base_model import BaseModel
from models.power import Power


class Character(BaseModel):
    def __init__(self, name="", powers=[], images_bucket_name="", health=None, subject=""):
        self.name = name
        self.powers = powers
        self.images_buckets_name = images_bucket_name
        self.health = health
        self.subject = subject

    def setup_powers(self):
        self.powers = [Power(**power) for power in self.powers]
