from jawiki_extractor.objects import WikiPage
from .title_verifier import TitleVerifier
from .line_verifier import LineVerifier
from .xml_affix_processor import XmlAffixProcessor
from .dsl_affix_processor import DslAffixProcessor


class StructureParser:

    @classmethod
    def run(cls, raw_page):
        page = WikiPage()
        texts = []
        state = "find_title"
        for line in raw_page.lines:
            if len(line) == 0:
                continue

            if state == "find_title":
                if XmlAffixProcessor.has_prefix(line, "title"):
                    title = XmlAffixProcessor.strip_affix(line, "title")

                    if not TitleVerifier.is_valid(title):
                        page.is_acceptable = False
                        return page

                    page.title = title
                    state = "find_text"

            elif state == "find_text":
                if XmlAffixProcessor.has_prefix(line, "text"):
                    line = XmlAffixProcessor.strip_prefix(line)
                    if DslAffixProcessor.has_prefix(line, "redirect"):
                        page.is_acceptable = False
                        return page
                    else:
                        texts.append(line)
                        state = "append_text"

            if state == "append_text":
                if XmlAffixProcessor.has_suffix(line, "text"):
                    line = XmlAffixProcessor.strip_suffix(line, "text")
                    if LineVerifier.is_acceptable(line):
                        texts.append(line)
                    page.text = "\n".join(texts)
                    return page
                else:
                    if LineVerifier.is_acceptable(line):
                        texts.append(line)
