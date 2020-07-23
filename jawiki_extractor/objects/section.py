import yaml
import os

_IGNORE_HEADERS_PATH = os.path.join(os.path.dirname(__file__), "../consts/ignore_section_headers.yml")
IGNORE_HEADERS = set(yaml.safe_load(open(_IGNORE_HEADERS_PATH)))


class Section:
    def __init__(self, header="", level=2):
        self.header = header
        self.texts = []
        self.level = level
        self.parent = None
        self.children = []
        self.is_acceptable = True

    def acceptable_iterator(self):
        if self.is_acceptable:
            yield self
            for child in self.children:
                yield from child.acceptable_iterator()

    def set_header(self, line):
        char_count = 0
        for char in line:
            if char != "=":
                break
            char_count += 1

        self.level = char_count
        self.header = line[char_count:-char_count].strip()

    def validate(self):
        self.is_acceptable = self.parent.is_acceptable and self.header not in IGNORE_HEADERS

    def __repr__(self):
        return f"Section(header={self.header}, children={self.children})"
