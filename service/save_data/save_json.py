import json


class OperationsJSON:
    def __init__(self):
        self.string_ = str()
        self.path = str()
        self.dict_ = {}

    def loads(self) -> None:
        """Parse string to dict"""
        self.dict_ = json.loads(self.string_)

    def load(self) -> None:
        """Read JSON file and add data to self.dict_"""
        with open(self.path) as path:
            self.dict_ = json.load(path)

    def dumps(self, indent: int) -> None:
        """Convert dict to json format with indents"""
        self.string_ = json.dumps(self.dict_, indent=indent, sort_keys=True)

    def dump(self, indent: int) -> None:
        """Write dict to JSON file"""
        with open(self.path, 'w') as json_file:
            json.dump(self.dict_, json_file, indent=indent, sort_keys=True)
