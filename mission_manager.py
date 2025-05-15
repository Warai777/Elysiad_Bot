# mission_manager.py
import time

class Mission:
    def __init__(self, mission_id, description, time_limit_seconds, is_main=False):
        self.mission_id = mission_id
        self.description = description
        self.is_main = is_main
        self.start_time = time.time()
        self.time_limit = time_limit_seconds
        self.completed = False
        self.failed = False

    def check_expired(self):
        if not self.completed and time.time() > self.start_time + self.time_limit:
            self.failed = True
            return True
        return False

    def complete(self):
        self.completed = True
        self.failed = False

class MissionManager:
    def __init__(self):
        self.active_missions = []

    def add_mission(self, mission):
        self.active_missions.append(mission)

    def get_active_missions(self):
        return [m for m in self.active_missions if not m.completed and not m.failed]

    def update_missions(self):
        for mission in self.active_missions:
            mission.check_expired()