import yaml
import os

_IGNORE_HEADERS_PATH = os.path.join(os.path.dirname(__file__), "../consts/ignore_section_headers.yml")
IGNORE_HEADERS = set(yaml.safe_load(open(_IGNORE_HEADERS_PATH)))

TOP_LEVEL = 2


class Section:
    def __init__(self, header="", level=TOP_LEVEL):
        self.header = header
        self.texts = []
        self.level = level
        self.parent = None
        self.children = []
        self.is_acceptable = True

    def set_header(self, line):
        char_count = 0
        for char in line:
            if char != "=":
                break
            char_count += 1

        self.level = char_count
        self.header = line[char_count:-char_count].strip()

    def set_parent(self, parent):
        parent.children.append(self)
        self.parent = parent

    def is_top_level(self):
        return self.level == TOP_LEVEL

    def validate(self):
        self.is_acceptable = (self.is_top_level() or self.parent.is_acceptable) \
                             and self.header not in IGNORE_HEADERS

    def __iter__(self):
        if self.is_acceptable:
            yield self
            for child in self.children:
                yield from child.acceptable_iterator()

    def __repr__(self):
        return f"Section(header={self.header}, level={self.level})"
