from jsonpath_rw import jsonpath, parse


class JsonExtractor():
    def __init__(self):
        pass

    @classmethod
    def extract_value(cls, json_object, json_path):
        json_path_expr = parse(json_path)
        match = json_path_expr.find(json_object)
        if len(match) > 0:
            return match[0].value
        else:
            return ''
