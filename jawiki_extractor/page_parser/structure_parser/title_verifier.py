import re


class TitleVerifier:
    IGNORE_PREFIXES = {
        "MediaWiki:",
        "Wikipedia:",
        "Template:",
        "Help:",
        "Portal:",
        "Category:",
        "ファイル:",
        "プロジェクト:",
        "必要とされている"

    }
    IGNORE_WORDS = {
        "一覧",
        "曖昧さ回避",
    }
    IGNORE_REGEX = {
        re.compile(r"^[0-9]+(月)?[0-9]*(日)?$"),
        re.compile(r"^(紀元前)?[0-9]+(年)?(代)?(世)?(紀)?$"),
    }

    @classmethod
    def is_valid(cls, title):
        return all(not title.startswith(prefix) for prefix in cls.IGNORE_PREFIXES) \
               and all(word not in title for word in cls.IGNORE_WORDS) \
               and all(not exp.match(title) for exp in cls.IGNORE_REGEX)
