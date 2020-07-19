
class WikiPage:
    def __init__(self):
        self.title = None
        self.texts = []
        self.is_acceptable = True

    def __repr__(self):
        return f"WikiPage(title={self.title} texts={self.texts})"
