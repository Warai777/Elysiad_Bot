...TRUNCATED...

    def autosave_if_needed(self):
        from time import time
        now = time()
        last = getattr(self, "_last_autosave", 0)
        if now - last > 60:
            self.autosave()
            self._last_autosave = now

...TRUNCATED...