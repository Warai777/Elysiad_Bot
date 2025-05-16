...TRUNCATED...

    def __init__(self, session_id):
        ...
        self.current_chapter_id = None  # Track unique chapter per phase

    def start_chapter(self, title):
        chapter = {
            "id": len(self.chapters) + 1,
            "title": title,
            "timestamp": datetime.utcnow().isoformat(),
            "content": []
        }
        self.chapters.append(chapter)
        self.current_chapter_index = len(self.chapters) - 1
        self.current_chapter_id = chapter["id"]
        self.log_journal(f"-- {title} begins --", type_="system", importance="high", tags=["chapter"])

...TRUNCATED...