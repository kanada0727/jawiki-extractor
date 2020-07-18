from dataclasses import dataclass, field
from typing import List

PAGE_HEADER = "  <page>\n"
PAGE_FOOTER = "  </page>\n"


@dataclass
class RawPage:
    lines: List[str] = field(default_factory=list)


class RawPageGenerator:
    def __init__(self, file_path):
        self.line_iterator = open(file_path)

    def __iter__(self):
        state = "find_page"
        lines = []
        for line in self.line_iterator:

            if state == "find_page":
                if line == PAGE_HEADER:
                    state = "append_line"

            elif state == "append_line":
                if line == PAGE_FOOTER:
                    yield RawPage(lines)
                    lines = []
                    state = "find_page"
                else:
                    lines.append(line.strip())
