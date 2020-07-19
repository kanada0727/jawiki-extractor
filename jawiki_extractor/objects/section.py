class Section:
    IGNORE_HEADERS = {
        "脚注",
        "外部リンク",
        "関連項目",
        "出典",
        "注釈",
        "脚注",
        "参考文献",
    }

    def __init__(self, header="", level=2):
        self.header = header
        self.texts = []
        self.level = level
        self.parent = None
        self.children = []
        self.is_acceptable = True

    def __iter__(self):
        yield self
        for child in self.children:
            yield from iter(child)

    def acceptable_iterator(self):
        if self.is_acceptable:
            yield self
            for child in self.children:
                yield from child.acceptable_iterator()

    def __repr__(self):
        return f"Section(header={self.header}, children={self.children})"

    def set_header(self, line):
        char_count = 0
        for char in line:
            if char != "=":
                break
            char_count += 1

        self.level = char_count
        self.header = line[char_count:-char_count].strip()

    def validate(self):
        self.is_acceptable = self.parent.is_acceptable and self.header not in self.IGNORE_HEADERS
