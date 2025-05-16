...TRUNCATED...

    def set_main_mission(self, description, duration_minutes=1440):
        from datetime import datetime, timedelta
        now = datetime.utcnow()
        self.main_mission = {
            "description": description,
            "start_time": now.isoformat(),
            "end_time": (now + timedelta(minutes=duration_minutes)).isoformat()
        }
        self.log_journal(f"Main mission assigned: {description}", type_="system", tags=["mission"])
        self.autosave()

    def check_main_mission_timer(self):
        from datetime import datetime
        if self.main_mission:
            end_time = datetime.fromisoformat(self.main_mission["end_time"])
            if datetime.utcnow() > end_time:
                self.log_journal("Main mission failed due to time expiration.", type_="system", tags=["failure"])
                self.main_mission = None
                self.autosave()

...TRUNCATED...