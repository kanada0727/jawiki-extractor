from dataclasses import dataclass


@dataclass
class WikiPage:
    title: str = ""
    text: str = ""
    is_acceptable: bool = True


class PageParser:
    @classmethod
    def parse(cls, raw_page):  # TODO: implement
        return WikiPage(
            title=raw_page.lines[0],
            text=raw_page.lines[0]
        )
