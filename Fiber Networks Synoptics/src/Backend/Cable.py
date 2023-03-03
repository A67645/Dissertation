class Cable:
    def __init__(self, entity=None, network="", cable_type="", identifier=""):
        self.identifier = identifier
        self.network = network
        self.cable_type = cable_type
        self.entity = entity
        self.length = 1000
        self.leftover = 0

    def set_identifier(self, identifier):
        self.identifier = identifier

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

    def get_identifier(self) -> str:
        return self.identifier

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
