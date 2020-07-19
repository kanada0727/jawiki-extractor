from jawiki_extractor.objects import WikiPage, Section
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

        return InitSection.run(line, page)


class InitSection:
    @classmethod
    def run(cls, line, page):
        section = Section()

        if DslAffixProcessor.has_affix(line, "header"):
            section.set_header(line)
            return cls._transition_process(page, section, lambda: PopulateSection)
        else:
            return cls._transition_process(page, section, lambda: PopulateSection.run(line, page))

    @staticmethod
    def _transition_process(page, section, transition_func):
        page.append_section(section)
        section.validate()
        if section.is_acceptable:
            return transition_func()
        else:
            return IgnoreSection


class IgnoreSection:
    @staticmethod
    def run(line, page):
        if DslAffixProcessor.has_affix(line, "header"):
            return InitSection.run(line, page)

        elif XmlAffixProcessor.has_suffix(line, "text"):
            return None
        else:
            return IgnoreSection


class PopulateSection:
    @staticmethod
    def run(line, page):
        if DslAffixProcessor.has_affix(line, "header"):
            return InitSection.run(line, page)
        elif XmlAffixProcessor.has_suffix(line, "text"):
            line = XmlAffixProcessor.strip_suffix(line, "text")
            if LineVerifier.is_acceptable(line):
                page.last_section.texts.append(line)
            return None
        else:
            if LineVerifier.is_acceptable(line):
                page.last_section.texts.append(line)
            return PopulateSection
