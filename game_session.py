...TRUNCATED...

    def advance_phase(self, new_phase):
        self.current_phase = new_phase
        self._log_phase_transition(new_phase)
        self._start_phase_chapter(new_phase)
        self.autosave()

    def _log_phase_transition(self, phase):
        self.log_journal(f"You have entered a new story phase: {phase}", type_="system", importance="medium", tags=["phase"])

    def _start_phase_chapter(self, phase):
        self.start_chapter(f"Phase – {phase}")

...TRUNCATED...