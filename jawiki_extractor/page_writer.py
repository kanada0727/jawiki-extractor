import json


class PageWriter:
    def __init__(self, file_path,  output_format="text"):
        self.file = open(file_path, "w")
        self.output_format = output_format
        self.write_func = self._decide_write_func()

    def run(self, page):
        self.write_func(page)

    def _decide_write_func(self):
        if self.output_format == "text":
            return self._write_text
        elif self.output_format == "json":
            return self._write_json
        else:
            raise RuntimeError

    def _write_text(self, page):
        self.file.write(page.text + "\n")

    def _write_json(self, page):
        dic = {
            "title": page.title,
            "text": page.text
        }
        line = json.dumps(dic, ensure_ascii=False)
        self.file.write(line + "\n")
