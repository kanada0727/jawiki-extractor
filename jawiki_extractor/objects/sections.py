from collections import defaultdict


class Sections:
    def __init__(self):
        self._sections = []
        self._levelwise_sections = defaultdict(list)

    def __iter__(self):
        for section in self._sections:
            if section.is_acceptable:
                yield section

    @property
    def last_section(self):
        return self._sections[-1]

    def append(self, section):
        self._sections.append(section)
        self._levelwise_sections[section.level].append(section)

        if not section.is_top_level():
            parent_section = self._levelwise_sections[section.level - 1][-1]
            section.set_parent(parent_section)

        section.validate()

    def __repr__(self):
        return "\n".join([str(section) for section in self])
