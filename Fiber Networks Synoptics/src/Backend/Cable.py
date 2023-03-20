class Cable:
    def __init__(self, entity):
        self.entity = entity  # Entidade do ezdxf do tipo LWPOLYLINE que consiste no cabo
        self.network = self.extract_network()  # Cabo Primário, Secundário ou Misto
        self.cable_type = self.extract_cable_type()  # ORAC vs ORAP
        self.length = 1000
        self.leftover = 0

    def extract_network(self) -> str:
        layer = self.entity.dxf.layer.split("-")
        return layer[1]

    def extract_cable_type(self) -> str:
        layer = self.entity.dxf.layer.split("-")
        return layer[2]

    def set_network(self, network):
        self.network = network

    def set_cable_type(self, cable_type):
        self.cable_type = cable_type

    def set_length(self, length):
        self.length = length

    def set_leftover(self, leftover):
        self.leftover = leftover

    def set_entity(self, entity):
        self.entity = entity

    def get_network(self) -> str:
        return self.network

    def get_cable_type(self) -> str:
        return self.cable_type

    def get_length(self) -> int:
        return self.length

    def get_leftover(self) -> int:
        return self.leftover

    def get_entity(self):
        return self.entity
