class Cable:
    def __init__(self):
        self.network = ""  # Rede primária (Cabos Primários), secundária (Cabos Secundários) ou mistos (Cabos Mistos)
        self.cable_type = ""  # ORAC, ORAP, EDP
        self.cable_name = ""  # ex: VDF-PEN15-95000
        self.length = 4000
        self.leftover = 10

    def set_network(self, network):
        self.network = network

    def set_cable_type(self, cable_type):
        self.cable_type = cable_type

    def set_cable_name(self, cable_name):
        self.cable_name = cable_name

    def set_length(self, length):
        self.length = length

    def set_leftover(self, leftover):
        self.leftover = leftover

    def get_network(self) -> str:
        return self.network

    def get_cable_type(self) -> str:
        return self.cable_type

    def get_length(self) -> int:
        return self.length

    def get_leftover(self) -> int:
        return self.leftover

