from .line_processor import LineProcessor


class LineVerifier:

    @classmethod
    def is_acceptable(cls, line):
        return (not LineProcessor.has_prefix(line, "decorations")) \
               and (not LineProcessor.equals(line, "horizontal_line"))
