# game_session.py

class GameSession:
    def __init__(self, player_id):
        self.player_id = player_id
        self.current_world = None
        self.current_year = None
        self.current_shard = None
        self.origin_essence = 0
        self.suspicion = 0
        self.tier = "Tier 9"
        self.inventory = []
        self.active_mission = None
        self.side_missions = []
        self.choice_log = []

    def to_dict(self):
        return self.__dict__

    def load_from_dict(self, data):
        self.__dict__.update(data)
