...TRUNCATED...

    def __init__(self, session_id):
        self.session_id = session_id
        self.origin_essence = 0
        self.suspicion = 0
        self.year = 0
        self.inventory = []
        self.journal = []
        self.unlocked_lore = []
        self.tier = 0
        self.strength = 5
        self.traits = ["basic_strength"]
        self.roles = []
        self.current_phase = "Intro"
        self.containers = [
            Container("Pockets", "starter", 2, {"length": 6, "width": 4, "height": 0.75, "unit": "in"})
        ]
        self.npc_memory = {}
        self.action_history = []
        self.chapters = []
        self.current_chapter_index = -1
        self.start_chapter("Prologue: Your Arrival")

    def advance_phase(self, new_phase):
        self.current_phase = new_phase
        self.start_chapter(f"Phase – {new_phase}")
        self.log_journal(f"You have entered a new story phase: {new_phase}", type_="system", importance="medium", tags=["phase"])
        self.autosave()

...TRUNCATED...