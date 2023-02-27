import json

class Product:
    def __init__(self, row):
        self.seq, \
        self.name, \
        self.price, \
        self.category, \
        self.vendor = row

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=4)
