from models.base_model import BaseModel
from models.power import Power


class Character(BaseModel):
    def __init__(self, name="", powers=[], images_buck_name="", health=None):
        self.name = name
        self.powers = powers
        self.images_buckets_name = images_buck_name
        self.health = health

    def setup_powers(self):
        self.powers = [Power(**power) for power in self.powers]
