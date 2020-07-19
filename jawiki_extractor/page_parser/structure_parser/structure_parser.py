from jawiki_extractor.objects import WikiPage
from .title_verifier import TitleVerifier
from .line_verifier import LineVerifier


TITLE_PREFIX = "<title>"
TITLE_SUFFIX = "</title>"
TEXT_PREFIX = "<text"
TEXT_SUFFIX = "</text>"
REDIRECT = "#REDIRECT"
REDIRECT_JA = "#転送"

TITLE_PREFIX_LENGTH = len(TITLE_PREFIX)
TITLE_SUFFIX_LENGTH = len(TITLE_SUFFIX)
TEXT_PREFIX_LENGTH = len(TEXT_PREFIX)
TEXT_SUFFIX_LENGTH = len(TEXT_SUFFIX)
REDIRECT_LENGTH = len(REDIRECT)
REDIRECT_JA_LENGTH = len(REDIRECT_JA)


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
                if cls._is_title_line(line):
                    title = cls._strip_title(line)

                    if not TitleVerifier.is_valid(title):
                        page.is_acceptable = False
                        return page

                    page.title = title
                    state = "find_text"

            elif state == "find_text":
                if cls._is_text_begin(line):
                    line = cls._strip_text_begin(line)
                    if cls._is_redirect(line):
                        page.is_acceptable = False
                        return page
                    else:
                        texts.append(line)
                        state = "append_text"

            if state == "append_text":
                if cls._is_text_end(line):
                    line = cls._strip_text_end(line)
                    if LineVerifier.is_acceptable(line):
                        texts.append(line)
                    page.text = "\n".join(texts)
                    return page
                else:
                    if LineVerifier.is_acceptable(line):
                        texts.append(line)

    @staticmethod
    def _is_text_end(line):
        return line[-TEXT_SUFFIX_LENGTH:] == TEXT_SUFFIX

    @staticmethod
    def _is_text_begin(line):
        return line[:TEXT_PREFIX_LENGTH] == TEXT_PREFIX

    @staticmethod
    def _is_redirect(line):
        return line[:REDIRECT_LENGTH] == REDIRECT or line[:REDIRECT_JA_LENGTH] == REDIRECT_JA

    @staticmethod
    def _is_title_line(line):
        return line[:TITLE_PREFIX_LENGTH] == TITLE_PREFIX

    @staticmethod
    def _strip_text_begin(line):
        return line[:TEXT_PREFIX_LENGTH]

    @staticmethod
    def _strip_title(line):
        return line[TITLE_PREFIX_LENGTH:-TITLE_SUFFIX_LENGTH]

    @staticmethod
    def _strip_text_end(line):
        return line[:-TITLE_SUFFIX_LENGTH]
