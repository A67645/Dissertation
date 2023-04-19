from Cable import Cable


class PDO:

    def __init__(self, entity):
        self.entity = entity
        self.identifier = entity.get_attrib_text("JFO_PDO")
        self.jso_zone = entity.get_attrib_text("TIPO")
        self.hp = entity.get_attrib_text("HP")
        self.output_cables = []
        self.input_cable = Cable()

    def add_output_cable(self, cable):
        self.output_cables.append(cable)
