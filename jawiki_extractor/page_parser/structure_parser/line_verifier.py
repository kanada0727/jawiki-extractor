from .dsl_affix_processor import DslAffixProcessor


class LineVerifier:

    @classmethod
    def is_acceptable(cls, line):
        return (not DslAffixProcessor.has_prefix(line, "decoration")) \
               and (not DslAffixProcessor.has_affix(line, "header")) \
               and (not cls._is_horizontal_line(line))

    @staticmethod
    def _is_header(line):
        return line[-2:] == "==" and line[:2] == "=="

    @staticmethod
    def _is_horizontal_line(line):
        return line == "----"
