...TRUNCATED...

    def __init__(self, session_id):
        ...
        self.main_mission = None
        self.side_missions = []

    def to_dict(self):
        return {
            ...
            "main_mission": self.main_mission,
            "side_missions": self.side_missions
        }

    def load_from_dict(self, data):
        ...
        self.main_mission = data.get("main_mission")
        self.side_missions = data.get("side_missions", [])

    def set_main_mission(self, description):
        self.main_mission = {
            "description": description,
            "start_time": datetime.utcnow().isoformat()
        }
        self.log_journal(f"Main mission assigned: {description}", type_="system", tags=["mission"])
        self.autosave()

    def add_side_mission(self, description):
        self.side_missions.append({
            "description": description,
            "start_time": datetime.utcnow().isoformat()
        })
        self.log_journal(f"Side mission added: {description}", type_="system", tags=["mission"])
        self.autosave()

...TRUNCATED...