from models.base_model import BaseModel


class Match(BaseModel):
    def __init__(self, match_id=None, player_count=0, started=False, turn=None, question_start_time=None, waiting_timeout_id=0):
        self.match_id = match_id
        self.player_count = player_count
        self.started = started
        self.turn = turn
        self.question_start_time = question_start_time
        self.waiting_timeout_id = waiting_timeout_id
