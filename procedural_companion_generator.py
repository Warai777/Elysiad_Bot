import random

# --- NAME PARTS ---
name_prefixes = ["Va", "Syl", "Ka", "Ar", "Ro", "Zai", "Ly", "Thae", "Maer", "Sol"]
name_suffixes = ["rin", "thas", "dra", "mir", "vorn", "lian", "reth", "syl", "dros", "ven"]

# --- PERSONALITIES ---
personalities = [
    "Bold", "Cautious", "Mysterious", "Reckless", "Kind", "Stoic", "Tactical", "Charming"
]

# --- TRAITS (inspired by famous worlds, fully original names) ---
special_traits = [
    "Soul Echo Partner",       # Inspired by Soul Eater
    "Shadow Apprentice",       # Inspired by Robin tactical copying
    "Voidstep Survivor",       # Inspired by Gojo untouchability
    "Fate Binder",             # Inspired by Death Note style "weakening"
    "Silent Vigil",            # Inspired by Itachi silent protection
    "Aether Architect",        # Inspired by FMA alchemy building
    "Breath of Dawn",          # Inspired by Demon Slayer breath styles
    "Stellar Pulse",           # Pure Elysiad cosmic theme
    "Dream Weaver",            # Elysiad original
    "Gravity Breaker"          # Gravity/fighting themes
]

# --- TYPES ---
companion_types = [
    "Assault", "Defender", "Support", "Healer", "Weapon Partner", "Mystic Bond"
]

class ProceduralCompanionGenerator:
    @staticmethod
    def generate_companion():
        # Randomly create a name
        name = random.choice(name_prefixes) + random.choice(name_suffixes)
        
        # Randomly pick a personality
        personality = random.choice(personalities)

        # Randomly pick a trait
        special_trait = random.choice(special_traits)

        # Randomly pick a type
        companion_type = random.choice(companion_types)

        # Generate base stats based on type
        if companion_type == "Assault":
            base_hp = random.randint(110, 140)
            attack = random.randint(15, 25)
            defense = random.randint(5, 10)
        elif companion_type == "Defender":
            base_hp = random.randint(120, 160)
            attack = random.randint(8, 12)
            defense = random.randint(15, 25)
        elif companion_type == "Healer":
            base_hp = random.randint(90, 110)
            attack = random.randint(5, 10)
            defense = random.randint(10, 15)
        elif companion_type == "Support":
            base_hp = random.randint(100, 120)
            attack = random.randint(10, 15)
            defense = random.randint(10, 15)
        elif companion_type == "Weapon Partner":
            base_hp = random.randint(100, 120)
            attack = random.randint(15, 20)
            defense = random.randint(10, 15)
        else:  # Mystic Bond
            base_hp = random.randint(100, 130)
            attack = random.randint(12, 18)
            defense = random.randint(12, 18)

        return {
            "name": name,
            "personality": personality,
            "special_trait": special_trait,
            "type": companion_type,
            "base_hp": base_hp,
            "attack": attack,
            "defense": defense,
            "loyalty": 50  # Start at neutral loyalty
        }
