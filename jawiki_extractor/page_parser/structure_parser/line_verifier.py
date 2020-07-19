
class LineVerifier:
    SECTION_CHARACTERS = {
        ";",  # description
        ":",  # indent
        "#",  # ordered list
        "*"   # unordered list
    }

    @classmethod
    def is_acceptable(cls, line):
        return (not cls._is_header(line)) and (not cls._is_horizontal_line(line)) and (not cls._has_section_identifier(line))

    @staticmethod
    def _is_header(line):
        return line[-2:] == "==" and line[:2] == "=="

    @staticmethod
    def _is_horizontal_line(line):
        return line == "----"

    @classmethod
    def _has_section_identifier(cls, line):
        return line[0] in cls.SECTION_CHARACTERS
