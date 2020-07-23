import yaml
import os


class _LineProcessor:
    def __init__(self):
        self.decorators = self._load_decorator_yaml()

    def _load_decorator_yaml(self):
        file_path = os.path.join(os.path.dirname(__file__), "../../consts/line_decorators.yml")
        dic = yaml.safe_load(open(file_path))
        self._parse_decorator_dict(dic)
        return dic

    def _parse_decorator_dict(self, decorator_dic):
        for key, value in decorator_dic.items():
            if isinstance(value, dict):
                self._parse_decorator_dict(value)
            elif key == "identifier":
                if isinstance(value, list):
                    decorator_dic[key] = tuple(value)
            elif key == "strip_func":
                decorator_dic[key] = getattr(self, "_" + value)

    def _remove_prefix_by_length(self, line, prefix_name):
        prefix_length = len(self.decorators["prefix"][prefix_name]["identifier"])
        return line[prefix_length:]
    
    @staticmethod
    def _remove_prefix_by_angle_close_bracket_offset(line, _):
        offset = line.find(">")
        return line[offset+1:]
    
    def _remove_prefix_until_continuous_char_end(self, line, prefix_name):
        decorator = set(self.decorators["prefix"][prefix_name]["identifier"])
        offset = 0
        for c in line:
            if c not in decorator:
                break
            offset += 1
        return line[offset:]

    def _remove_suffix_by_length(self, line, suffix_name):
        suffix_length = len(self.decorators["suffix"][suffix_name]["identifier"])
        return line[:-suffix_length]

    def has_prefix(self, line,  prefix_name):
        return line.startswith(self.decorators["prefix"][prefix_name]["identifier"])
    
    def has_suffix(self, line, suffix_name):
        return line.endswith(self.decorators["suffix"][suffix_name]["identifier"])

    def has_affix(self, line, affix_name):
        return self.has_prefix(line, affix_name) and self.has_suffix(line, affix_name)

    def equals(self, line, alias_name):
        return line == self.decorators["alias"][alias_name]

    def strip_prefix(self, line, prefix_name):
        return self.decorators["prefix"][prefix_name]["strip_func"](line, prefix_name)

    def strip_suffix(self, line, suffix_name):
        return self.decorators["suffix"][suffix_name]["strip_func"](line, suffix_name)

    def strip_affix(self, line, affix_name):
        line = self.strip_prefix(line, affix_name)
        line = self.strip_suffix(line, affix_name)
        return line


LineProcessor = _LineProcessor()
