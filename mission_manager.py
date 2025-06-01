import time
from game.timeline_manager import TimelineShard

class Mission:
    def __init__(self, mission_id, description, time_limit_seconds, is_main=False, world="Unknown", phase="Unknown"):
        self.mission_id = mission_id
        self.description = description
        self.is_main = is_main
        self.start_time = time.time()
        self.time_limit = time_limit_seconds
        self.completed = False
        self.failed = False
        self.world = world
        self.phase = phase

    def check_expired(self):
        if not self.completed and time.time() > self.start_time + self.time_limit:
            self.failed = True
            return True
        return False

    def complete(self, session=None):
        self.completed = True
        self.failed = False
        if session and hasattr(session, "enter_new_world"):
            # Unlock world lore at mission completion
            available = session.current_world
            if available:
                session.enter_new_world(available)
                session.log_journal("Something buried was revealed by your success...", type_="lore", importance="medium", tags=["mission", "discovery"])

class MissionManager:
    def __init__(self, player_name):
        self.active_missions = []
        self.player_name = player_name
        self.shard_log = TimelineShard("Default", 1500)

    def add_mission(self, mission):
        self.active_missions.append(mission)

    def get_active_missions(self):
        return [m for m in self.active_missions if not m.completed and not m.failed]

    def update_missions(self):
        for mission in self.active_missions:
            expired = mission.check_expired()
            if expired:
                self.log_result(mission, "Failed")
            elif mission.completed:
                self.log_result(mission, "Completed")

    def log_result(self, mission, result):
        event_text = f"Mission {mission.mission_id} ({mission.description}) {result}"
        self.shard_log.log_event(
            self.player_name, event_text,
            year=1500,  # Placeholder, would link to current session year
            phase=mission.phase
        )