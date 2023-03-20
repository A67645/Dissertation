class JFO:

    def __init__(self, entity):
        self.entity = entity
        self.identifier = entity.get_attrib("JFO_PDO")
        self.trailing_cable_identifier = entity.get_attrib("CABO_PRIMARIO")
        self.trailing_cable_attributes = entity.get_attrib("CABO_CAP_COP")

    def get_identifier(self) -> str:
        return self.identifier

    def get_trailing_cable_identifier(self) -> str:
        return self.trailing_cable_identifier

    def set_identifier(self, identifier: str):
        self.identifier = identifier

    def set_trailing_cable_identifier(self, cable_identifier: str):
        self.trailing_cable_identifier = cable_identifier
