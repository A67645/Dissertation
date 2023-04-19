from Cable import Cable


class JSO:

    def __init__(self, entity):
        self.entity = entity
        self.identifier = entity.get_attrib_text("TIPO")
        self.hp = entity.get_attrib_text("HP")
        self.output_cables = []
        self.input_cable = Cable()

    def add_output_cable(self, cable):
        self.output_cables.append(cable)

    def get_identifier(self) -> str:
        return self.identifier

    def get_trailing_cable_identifier(self) -> str:
        return self.trailing_cable_identifier

    def get_hp(self) -> int:
        return self.hp

    def set_identifier(self, identifier):
        self.identifier = identifier

    def set_trailing_cable_identifier(self, cable_identifier):
        self.trailing_cable_identifier = cable_identifier

    def set_hp(self, hp):
        self.hp = hp
