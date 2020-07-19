from jawiki_extractor.objects import WikiPage
from .title_verifier import TitleVerifier
from .line_verifier import LineVerifier
from .xml_affix_processor import XmlAffixProcessor
from .dsl_affix_processor import DslAffixProcessor


class StructureParser:
    @classmethod
    def run(cls, raw_page):
        page = WikiPage()
        line_parser = StatefulLineParser()
        for line in raw_page.lines:
            if len(line) == 0:
                continue

            line_parser.run(line, page)
            if line_parser.current_state is None:
                return page


class StatefulLineParser:
    def __init__(self):
        self.current_state = FindTitle

    def run(self, line, page):
        if self.current_state:
            self.current_state = self.current_state.run(line, page)

    def is_finished(self):
        # decide not to use this func to reduce costs of function call
        return self.current_state is None


class FindTitle:
    @staticmethod
    def run(line, page):
        if not XmlAffixProcessor.has_prefix(line, "title"):
            return FindTitle

        title = XmlAffixProcessor.strip_affix(line, "title")

        if not TitleVerifier.is_valid(title):
            page.is_acceptable = False
            return None

        page.title = title
        return FindText


class FindText:
    @staticmethod
    def run(line, page):
        if not XmlAffixProcessor.has_prefix(line, "text"):
            return FindText

        line = XmlAffixProcessor.strip_prefix(line)

        if DslAffixProcessor.has_prefix(line, "redirect"):
            page.is_acceptable = False
            return None

        return AppendText.run(line, page)


class AppendText:
    @classmethod
    def run(cls, line, page):
        if not XmlAffixProcessor.has_suffix(line, "text"):
            if LineVerifier.is_acceptable(line):
                page.texts.append(line)
            return AppendText

        line = XmlAffixProcessor.strip_suffix(line, "text")
        if LineVerifier.is_acceptable(line):
            page.texts.append(line)
        return None

    @staticmethod
    def _append_line(line, page):
        # decide not to use this func to reduce costs of function call
        if LineVerifier.is_acceptable(line):
            page.texts.append(line)
