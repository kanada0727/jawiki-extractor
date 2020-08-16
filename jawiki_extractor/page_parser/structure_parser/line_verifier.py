from .line_processor import LineProcessor


class LineVerifier:

    @classmethod
    def is_acceptable(cls, line):
        return not LineProcessor.equals(line, "horizontal_line")
