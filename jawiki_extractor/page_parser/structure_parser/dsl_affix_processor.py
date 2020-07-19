PREFIXES = {
    "redirect": ("#REDIRECT", "#転送"),
    "decoration": (
        ";",  # description
        ":",  # indent
        "#",  # ordered list
        "*"  # unordered list
    ),
    "header": "==",
}

SUFFIXES = {
    "header": "=="
}


class DslAffixProcessor:
    @staticmethod
    def has_prefix(line, prefix_name):
        return line.startswith(PREFIXES[prefix_name])

    @staticmethod
    def has_suffix(line, suffix_name):
        return line.endswith(SUFFIXES[suffix_name])

    @classmethod
    def has_affix(cls, line, affix_name):
        return cls.has_prefix(line, affix_name) and cls.has_suffix(line, affix_name)
