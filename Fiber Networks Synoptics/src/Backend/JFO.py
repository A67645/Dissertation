from Cable import Cable


class JFO:

    def __init__(self, entity):
        self.entity = entity
        self.identifier = entity.get_attrib_text("JFO#")
        self.output_cables = []
        self.input_cable = Cable()

    def add_output_cable(self, cable):
        self.output_cables.append(cable)

    def get_identifier(self) -> str:
        return self.identifier

    def set_identifier(self, identifier: str):
        self.identifier = identifier
