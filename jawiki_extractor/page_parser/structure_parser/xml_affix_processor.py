PREFIXES = {
    "title": "<title",
    "text": "<text",
}
SUFFIXES = {
    "title": "</title>",
    "text": "</text>",
}


class XmlAffixProcessor:
    @staticmethod
    def has_prefix(line, prefix_name):
        return line.startswith(PREFIXES[prefix_name])

    @staticmethod
    def has_suffix(line, suffix_name):
        return line.endswith(SUFFIXES[suffix_name])

    @staticmethod
    def strip_prefix(line):
        end_offset = line.find(">")
        return line[end_offset+1:]

    @staticmethod
    def strip_suffix(line, suffix_name):
        return line[:-len(SUFFIXES[suffix_name])]

    @classmethod
    def strip_affix(cls, line, suffix_name):
        line = cls.strip_prefix(line)
        line = cls.strip_suffix(line, suffix_name)
        return line
