class Central:

    def __init__(self, entity):
        self.entity = entity
        self.trailing_cables = list()
        self.identifier = entity.get_attrib("CENTRAL")

    def set_trailing_cable(self, cables):
        for cable in cables:
            self.trailing_cables.append(cable)

    def set_identifier(self, identifier):
        self.identifier = identifier

    def set_entity(self, entity):
        self.entity = entity

    def get_entity(self):
        return self.entity

    def get_trailing_cable(self) -> list:
        return self.trailing_cables

    def get_identifier(self) -> str:
        return self.identifier
