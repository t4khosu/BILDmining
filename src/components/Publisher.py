class Publisher:
    def __init__(self, meta):
        self.type = meta['publisher']['@type']
        self.name = meta['publisher']['name']