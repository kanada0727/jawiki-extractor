from .sections import Sections


class WikiPage:
    def __init__(self):
        self.title = None
        self.is_acceptable = True
        self.sections = Sections()

    def get_all_texts(self):
        lines = []
        for section in self.sections:
            lines.extend(section.texts)
        return "\n".join(lines)

    def __repr__(self):
        return f"WikiPage(title={self.title} section={self.sections})"
