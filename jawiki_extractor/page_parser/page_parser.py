from jawiki_extractor.objects import WikiPage


class PageParser:
    @classmethod
    def parse(cls, raw_page):  # TODO: implement
        return WikiPage(
            title=raw_page.lines[0],
            text=raw_page.lines[0]
        )
