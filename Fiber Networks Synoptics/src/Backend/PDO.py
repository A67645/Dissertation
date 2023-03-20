class PDO:

    def __init__(self, entity):
        self.entity = entity
        self.identifier = entity.get_attrib("JSO_PDO")
        self.jso_zone = entity.get_attrib("TIPO")
        self.hp = entity.get_attrib("HP")
        self.trailing_cable_attributes = entity.get_attrib("CABO_CAP_COP")
