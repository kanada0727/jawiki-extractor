from dataclasses import dataclass


@dataclass
class WikiPage:
    title: str = ""
    text: str = ""
    is_acceptable: bool = True
