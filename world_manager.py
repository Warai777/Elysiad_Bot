...EXISTING CODE...

    def apply_world_effects(self, decision, session):
        effects_log = []
        if "war" in decision.lower():
            effects_log.append("Tensions rise across the region. Armies are repositioned.")
            session.suspicion += 10
        elif "alliance" in decision.lower():
            effects_log.append("New alliances are formed. Political maps shift subtly.")
        elif "artifact" in decision.lower():
            effects_log.append("The discovery of a relic sends shockwaves across guilds.")
        elif "death" in decision.lower():
            effects_log.append("Your act echoes through history. The world takes notice.")
            session.suspicion += 25
        return effects_log