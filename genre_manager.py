class GenreManager:
    def __init__(self):
        self.available_genres = [
            "Happy",
            "Mysterious",
            "Grimdark",
            "Surreal",
            "Epic",
            "Fantasy",
            "Sci-Fi",
            "Horror",
            "Tragic Poetic",
            "Dark Heroism"
        ]

    def get_genre_style(self, genre):
        styles = {
            "Happy": "bright, hopeful, colorful imagery",
            "Mysterious": "foggy, cautious, secretive atmosphere",
            "Grimdark": "bleak, brutal, despairing tone",
            "Surreal": "dreamlike, absurd, reality-warped style",
            "Epic": "grand, sweeping, legendary scale",
            "Fantasy": "magical, classic mythic worlds",
            "Sci-Fi": "cold, high-tech, futuristic or dystopian tone",
            "Horror": "fear-driven, visceral dread, darkness everywhere",
            "Tragic Poetic": "beautiful sadness, memory and loss",
            "Dark Heroism": "grim determination, noble suffering"
        }
        return styles.get(genre, "mysterious and unknown")
