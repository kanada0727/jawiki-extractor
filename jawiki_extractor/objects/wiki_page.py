from collections import defaultdict

from .section import Section


class WikiPage:
    def __init__(self):
        self.title = None
        self.is_acceptable = True
        self.root_section = Section(header="<root>", level=1)
        self.levelwise_sections = defaultdict(list)
        self.levelwise_sections[1].append(self.root_section)
        self.last_section = None

    def append_section(self, section):
        self.last_section = section
        self.levelwise_sections[section.level].append(section)
        parent_section = self.levelwise_sections[section.level-1][-1]
        parent_section.children.append(section)
        section.parent = parent_section

    def __repr__(self):
        return f"WikiPage(title={self.title} section={self.root_section})"
