from genre_manager import GenreManager

genre_manager = GenreManager()

class StoryEngine:
    def __init__(self, genre):
        self.genre = genre

    def generate_story_intro(self, world_name):
        style = genre_manager.get_genre_style(self.genre)

        intro = f"In the realm of <b>{world_name}</b>, the air is filled with {style}.<br>"
        intro += "You feel the weight of countless choices ahead.<br>"
        intro += "Some will lead to glory, some to ruin... and some to secrets never meant to be uncovered.<br>"
        intro += "Your journey begins now.<br>"

        return intro
